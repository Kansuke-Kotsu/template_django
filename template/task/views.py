from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from .models import Task

# for User Authorization
from .forms import AccountForm # ユーザーアカウントフォーム
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
class TaskView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
            params = {"UserID":request.user, 'tasks': tasks}
        if not request.user.is_authenticated:
            params = {"UserID":request.user,}
        return render(request, "index.html", context=params)

def check_task_request(request: HttpRequest) -> None:
    if request.method != 'POST':
        raise Http404('Request method is not POST.')

    user=request.user
    if not user.is_authenticated:
        raise Http404('User is not authenticated.')


def create_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)
    name = request.POST.get('name')
    if name is None:
        Http404('Task name is not set.')
    task = Task(user=request.user, name=name)
    task.save()
    return HttpResponseRedirect('../../')

def update_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)
    id_ = request.POST.get('id')
    name = request.POST.get('name')
    if id is None or name is None:
        Http404('Task id or name is not set.')
    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be edited.")
    task.name = name
    task.save()
    return HttpResponseRedirect('../../')


def delete_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)
    id_ = request.POST.get('id')
    if id is None:
        Http404('Task id is not set.')
    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be edited.")
    task.delete()
    return HttpResponseRedirect('../../')

# create account
class  AccountRegistration(TemplateView):
    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        }
    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["AccountCreate"] = False
        return render(request,"register.html",context=self.params)
    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        # フォーム入力の有効検証
        if self.params["account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # フォーム入力のユーザーID・パスワード取得
            ID = account.username
            Pass = account.password
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()
            # アカウント作成情報更新
            self.params["AccountCreate"] = True
            # 初回ログイン用にデータ保存
            user = authenticate(username=ID, password=Pass)
            login(request, user)   
            return HttpResponseRedirect(reverse('index.html'))
        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)    
            return render(request,"register.html",context=self.params)

# ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')
        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)
        print(user)
        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('index.html'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'login.html')

#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('index.html'))

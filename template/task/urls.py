from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", TaskView.as_view(), name="index.html"),
    path("register", views.AccountRegistration.as_view(), name="Register"),
    path("login", views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path('task/create/', views.create_task, name='create_task'),
    path('task/update/', views.update_task, name='update_task'),
    path('task/delete/', views.delete_task, name='delete_task'),
]

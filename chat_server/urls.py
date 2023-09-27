from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.ChatView.as_view(), name='chat'),
    path('xy/logintochat/', views.LoginToChat, name='loginchat'),
]
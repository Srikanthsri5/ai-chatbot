from django.urls import path
from .views import main, auth

urlpatterns =[
    path('',main.home, name='home'),
    path('home',main.chatbot, name='chatbot'),
    path('delete_chat/<int:chat_id>/', main.delete_chat, name='delete_chat'),
    path('login',auth.login, name='login'),
    path('register',auth.register, name='register'),
    path('logout',auth.logout, name='logout')
]

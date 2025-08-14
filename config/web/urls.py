from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('new/', views.new_chat, name="new_chat"),
    path('<int:pk>', views.chat_view, name="chat")
]

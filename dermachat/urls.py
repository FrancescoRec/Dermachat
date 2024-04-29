from django.urls import path
from . import views
from .chatbot import chatbot  

urlpatterns = [
    path("images/", views.upload_image, name='upload_image'), 
    path("chatbot/", chatbot, name='chatbot'),  
]

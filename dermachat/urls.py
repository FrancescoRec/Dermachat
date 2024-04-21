from django.urls import path
from . import views

urlpatterns = [
    path("", views.dermachat, name='upload_image') 
]


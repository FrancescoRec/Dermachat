from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_classification_view, name='doctor_interface'), 
    path("images/", views.get_images, name='images')

]
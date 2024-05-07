from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_function, name='doctor_interface'), 

]
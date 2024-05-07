from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def doctor_function(request):
    return HttpResponse("Hello, Doctor Perro!")
from django.shortcuts import render

# Create your views here.
def doctor_function(request):
    return render(request, 'doctor_interface.html')
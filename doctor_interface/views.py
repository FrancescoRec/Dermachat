
from django.shortcuts import render, redirect
from .models import DoctorSelection

def doctor_interface(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        skin_tone = request.POST.get('skin_tone', '')
        melanoma = request.POST.get('melanoma', False)
        
        DoctorSelection.objects.create(user_id=user_id, skin_tone=skin_tone, melanoma=melanoma)
        
        return redirect('doctor_interface') 
    
    return render(request, 'doctor_interface.html')

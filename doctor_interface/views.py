from django.shortcuts import render, redirect
from dermachat.models import ImageMetadata
from .models import DoctorClassification
from django.core.files.base import ContentFile
import os 



def get_images(request):
    # request to get the images from the database (it will connect to s3 for some magical spell)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        image = ImageMetadata.objects.filter(user_id=user_id).first()
        return render(request, 'doctor_interface.html', {'image': image, 'user_id': user_id})



def doctor_classification_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id_')
        skin_tone = request.POST.get('skin_tone')
        malignant = request.POST.get('malignant') == 'true'

        # Retrieve the image_id from ImageMetadata
        image_metadata = ImageMetadata.objects.filter(user_id=user_id).first()



        # Create DoctorClassification instance with retrieved image_id
        DoctorClassification.objects.create(
            user_id=user_id,
            skin_tone=skin_tone,
            malignant=malignant,
            image=ContentFile(image_metadata.image.read(), name=os.path.basename(image_metadata.image.name))

        )
        
        # Redirect back to the doctor page
        return redirect('doctor_interface')

    return render(request, 'doctor_interface.html')


from django.shortcuts import render, redirect
from dermachat.models import ImageMetadata
from django.db.models import Case, When, Value, CharField
from .models import DoctorClassification
from django.core.files.base import ContentFile
import os 


# Prendi le immagini e metti anche la prediction
def get_images(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
    else:
        user_id = request.GET.get('user_id')

    image = ImageMetadata.objects.filter(user_id=user_id).first()
    prediction = image.prediction
    return render(request, 'doctor_interface.html', {'image': image,
                                                        'user_id': user_id,
                                                        'prediction': round(prediction,4)})
    

# Aggiungi le immagini al database
def doctor_classification_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id_')
        skin_tone = request.POST.get('skin_tone')
        malignant = request.POST.get('malignant') == 'true'

        image_metadata = ImageMetadata.objects.filter(user_id=user_id).first()

        DoctorClassification.objects.create(
            user_id=user_id,
            skin_tone=skin_tone,
            malignant=malignant,
            image=ContentFile(image_metadata.image.read(), name=os.path.basename(image_metadata.image.name)),
            prediction= ImageMetadata.objects.filter(user_id=user_id).first().prediction

        )
        
        return redirect('doctor_interface')

    return render(request, 'doctor_interface.html')

# Mostra le immagini che sono state classificate e anche il livello di predizione
# La ragazza bionda che ha rubato il mio codice non sa neanche di cosa sto parlando
def table_view(request):

    directory = 'models/image_models/'
    
    pkl_file_name = ''
    for file in os.listdir(directory):
        if file.endswith('.pth'):
            pkl_file_name = os.path.join(directory, file)
            break
    

    data = ImageMetadata.objects.exclude(user_id__in=DoctorClassification.objects.values('user_id')).annotate(
        severity=Case(
            When(prediction__gte=0, prediction__lte=0.40, then=Value('Low')),
            When(prediction__gte=0.41, prediction__lte=0.59, then=Value('Moderate')),
            When(prediction__gte=0.60, prediction__lte=1, then=Value('High')),
            output_field=CharField(),
        )
    ).order_by('-prediction')
    
    context = {
        'data': data,
        'pkl_file_name': pkl_file_name.replace('models/image_models/', '').replace('.pth', '')
    }
    
    return render(request, 'table_view.html', context)
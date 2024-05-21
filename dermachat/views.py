from django.shortcuts import render

from .models import ImageMetadata
from .forms import ImageUploadForm
from .helper import obtain_prediction    
    
def upload_image(request):
    """Upload an image and return the prediction and upload the image to the database"""

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            prediction = obtain_prediction(image)
            # predicted_class = "Melanoma" if prediction > 0.5 else "No Melanoma"
            ImageMetadata.objects.create(image=image, prediction=prediction)
            return render(
                request,
                'upload_image.html',
                {
                    'form': form,
                    'image': ImageMetadata.image
                }
                
            )
    form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})
    




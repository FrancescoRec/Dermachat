from django.shortcuts import render

import cv2
import numpy as np
import torch
from torchvision import transforms
import timm
import os
from io import BytesIO

from .models import ImageMetadata
from .forms import ImageUploadForm



#  upload the image on the app
#  resize the image 
#  obtain the results of the prediction using the pkl.model
#  adding to the database the image with all the ImageMetadata fields
#  the user get the prediction of the image



def get_model():
    """Load the model from the local file system and return it"""
    model_name = 'Xception'
    local_model_path = os.path.join('models', 'image_models', f'{model_name}_model.pth')

    model = timm.create_model('legacy_xception', pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 2)  

    checkpoint = torch.load(local_model_path)
    model.load_state_dict(checkpoint)

    model.eval()

    return model


def preprocess_image(image):
    """Preprocess the image to be compatible with the model"""
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = transform(image)
    return image.unsqueeze(0)  



def obtain_prediction(image):
    """Modify the reuqest_image Obtain the prediction for the uploaded image and return it as a string"""
    image_bytes_io = image.read()
    image_data = cv2.imdecode(np.frombuffer(image_bytes_io, np.uint8), cv2.IMREAD_COLOR)
    image_tensor = preprocess_image(image_data)
    with torch.no_grad():
        model = get_model()
        output = model(image_tensor)
        probabilities = torch.sigmoid(output)[0]
        prob_true = probabilities[1].item()
        return prob_true
        

    
def upload_image(request):
    """Upload an image and return the prediction and upload the image to the database"""

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            prediction = obtain_prediction(image)
            predicted_class = "Melanoma" if prediction > 0.5 else "No Melanoma"
            ImageMetadata.objects.create(image=image)
            return render(
                request,
                'upload_image.html',
                {
                    'prediction_class': predicted_class,
                    'prediction_value': prediction,
                    'form': form
                }
                
            )

    # GET
    form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})
    




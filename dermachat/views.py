# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import timm
import os
import uuid
from datetime import datetime

from io import BytesIO
from .models import ImageMetadata

model_name = 'Xception'
local_model_path = os.path.join('models', 'image_models', f'{model_name}_model.pth')

# Initialize Xception model
model = timm.create_model('legacy_xception', pretrained=False)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)  

# Load model state dictionary from the locally downloaded file
checkpoint = torch.load(local_model_path)
model.load_state_dict(checkpoint)

# Set model to evaluation mode
model.eval()

# Function to preprocess the image
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = transform(image)
    return image.unsqueeze(0)  

def upload_image(request):
    # mke the function all the form
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            image_data = np.frombuffer(image_file.read(), np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # Perform inference
            image_tensor = preprocess_image(image)
            with torch.no_grad():
                output = model(image_tensor)
                probabilities = torch.sigmoid(output)[0]
                prob_true = probabilities[1].item()
                predicted_class = "Melanoma" if prob_true > 0.5 else "No Melanoma"


            image_file_like = BytesIO(image_data)
            image_data = ImageMetadata(image=image_file_like)
            image_data.save()

            # Save in the s3 bucket

            # Initialize the S3 client:

            s3 = boto3.client('s3')

            # Declare bucket file variables:
            folder_name = 'raw_data/nonlabelled_images/'

               



                    
                    
                  
        

            # Return the prediction as JSON response
            return JsonResponse({'predicted_class': predicted_class, 'prob_true': prob_true})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

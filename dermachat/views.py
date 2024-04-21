# from pipino_doctorino.settings import Credentials

# credentials = Credentials()
# AWS_ACCESS_KEY_ID = credentials.AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY = credentials.AWS_SECRET_ACCESS_KEY
# AWS_SECRET_TOKEN = credentials.AWS_SECRET_TOKEN
# AWS_STORAGE_BUCKET_NAME = credentials.AWS_STORAGE_BUCKET_NAME
# AWS_STORAGE_PATH = credentials.AWS_STORAGE_PATH
# AWS_PICKLE_MODEL = credentials.AWS_PICKLE_MODEL

from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import timm
import boto3
import os
import datetime

from pipino_doctorino.settings import Credentials

s3 = boto3.client('s3')

# Assuming credentials contains AWS credentials
credentials = Credentials()
model_path = credentials.AWS_STORAGE_PATH
bucket_name = credentials.AWS_STORAGE_BUCKET_NAME

local_model_dir = 'models'

# Create the local directory if it doesn't exist
if not os.path.exists(local_model_dir):
    os.makedirs(local_model_dir)

# Local path to save the model
local_model_path = os.path.join(local_model_dir, os.path.basename(model_path))

# Initialize S3 client
s3 = boto3.client('s3')

# Check if the local model file exists
if os.path.exists(local_model_path):
    # Get last modified date of local model file
    local_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(local_model_path))
    
    # Get last modified date of model file on S3
    response = s3.head_object(Bucket=bucket_name, Key=model_path)
    s3_last_modified = response['LastModified'].replace(tzinfo=None)

    # Compare last modified dates
    if s3_last_modified > local_last_modified:
        # Download the newer version from S3
        s3.download_file(bucket_name, model_path, local_model_path)
else:
    # If the local file doesn't exist, download it from S3
    s3.download_file(bucket_name, model_path, local_model_path)

# Initialize Xception model
model = timm.create_model('legacy_xception', pretrained=False)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)  # Modify fully connected layer for your task

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
    return image.unsqueeze(0)  # Add batch dimension

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded image
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

            # Return the prediction as JSON response
            return JsonResponse({'predicted_class': predicted_class, 'prob_true': prob_true})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

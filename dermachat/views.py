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

# def download_model_from_s3(bucket_name, key, local_file_path):
#     s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
#                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#                          aws_session_token=AWS_SECRET_TOKEN)
#     try:
#         response = s3.get_object(Bucket=bucket_name, Key=key)
#         with open(local_file_path, 'wb') as f:
#             f.write(response['Body'].read())
#         return True
#     except Exception as e:
#         print(f"Error downloading model file from S3: {e}")
#         return False

# Load the Xception model
model = timm.create_model('legacy_xception', pretrained=False)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)
checkpoint = torch.load('models/Xception_model.pth')
model.load_state_dict(checkpoint)
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

def dermachat(request):
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

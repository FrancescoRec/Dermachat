from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import timm
import os
# import datetime
from .helpers import predict_class, get_response, load_data, process_symptoms
from pipino_doctorino.settings import Credentials

# # Assuming credentials contains AWS credentials
# try:
#     credentials = Credentials()
#     model_path = credentials.AWS_STORAGE_PATH
#     bucket_name = credentials.AWS_STORAGE_BUCKET_NAME
# except AttributeError:
#     model_path = 'models/cnn/Xception_model.pth'  
#     bucket_name = None

# local_model_dir = 'models/cnn'

# # Create the local directory if it doesn't exist
# if not os.path.exists(local_model_dir):
#     os.makedirs(local_model_dir)

# # Local path to save the model
# local_model_path = os.path.join(local_model_dir, os.path.basename(model_path))

# testing = True

# if not testing and bucket_name:
#     try:
#         import botocore
#         import boto3
#         # Initialize S3 client
#         s3 = boto3.client('s3')

#         # Check if the local model file exists
#         if os.path.exists(local_model_path):
#             # Get last modified date of local model file
#             local_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(local_model_path))

#             try:
#                 # Get last modified date of model file on S3
#                 response = s3.head_object(Bucket=bucket_name, Key=model_path)
#                 s3_last_modified = response['LastModified'].replace(tzinfo=None)

#                 # Compare last modified dates
#                 if s3_last_modified > local_last_modified:
#                     # Download the newer version from S3
#                     s3.download_file(bucket_name, model_path, local_model_path)
#             except botocore.exceptions.ClientError as e:
#                 if e.response['Error']['Code'] == 'NoSuchKey':
#                     print("S3 not found")
#                 else:
#                     print("An error occurred with botocore:", e)
#                     # Fallback to using the model in the models folder locally
#                     raise e
#         else:
#             # If the local file doesn't exist, download it from S3
#             s3.download_file(bucket_name, model_path, local_model_path)

#     except (ImportError, botocore.exceptions.NoCredentialsError, botocore.exceptions.ClientError) as e:
#         print("AWS credentials not found or error occurred. Falling back to local resources.")
#         bucket_name = None



model_name = 'Xception'
local_model_path = os.path.join('models', 'cnn', f'{model_name}_model.pth')

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
    return image.unsqueeze(0)  


def dermachat_view(request):
    # Handle image upload functionality
    if request.method == 'POST' and 'image' in request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            image_data = np.frombuffer(image_file.read(), np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # Perform image classification inference
            image_tensor = preprocess_image(image)
            with torch.no_grad():
                output = model(image_tensor)
                probabilities = torch.sigmoid(output)[0]
                prob_true = probabilities[1].item()
                predicted_class = "Melanoma" if prob_true > 0.5 else "No Melanoma"

            # Return the image classification prediction as JSON response
            return JsonResponse({'predicted_class': predicted_class, 'prob_true': prob_true})

    # Handle chatbot functionality
    elif request.method == 'POST' and ('user_input' in request.POST or 'selected_symptoms' in request.POST):
        # Handle user input for chatbot
        user_input = request.POST.get('user_input')
        if user_input:
            predicted_class = predict_class(user_input)
            if predicted_class == "medical_consultation":
                request.session['medical_consultation'] = True
            else:
                response = get_response(predicted_class)
                return JsonResponse({'message': response})

        # Handle symptom submission for chatbot
        selected_symptoms = request.POST.getlist('selected_symptoms')
        if selected_symptoms:
            process_symptoms(selected_symptoms)
            request.session['medical_consultation'] = False
            return JsonResponse({'success': True})

    # Load initial data for chatbot
    symptoms, _, _ = load_data()
    conversation_history = []  # Load conversation history from session or database if needed

    # Render the combined template with necessary context data
    return render(request, 'dermachat.html', {
        'form': ImageUploadForm(),  # Pass the image upload form
        'symptoms': symptoms,       # Pass the symptoms data for chatbot
        'conversation_history': conversation_history,  # Pass conversation history data
    })

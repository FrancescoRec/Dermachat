
from django.shortcuts import render, redirect
from .models import DoctorSelection

import boto3

def doctor_interface(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        skin_tone = request.POST.get('skin_tone', '')
        melanoma = request.POST.get('melanoma', False)
        
        # Retrieve image filenames associated with the user_id from S3 bucket
        image_filenames = get_user_images_from_s3(user_id)
        
        # Pass image filenames to the template for display
        return render(request, 'doctor_interface.html', {'image_filenames': image_filenames})
    
    return render(request, 'doctor_interface.html')

def get_user_images_from_s3(user_id):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Specify S3 bucket and folder
    s3_bucket = 'provafinalproject'
    folder_name = 'raw_data/nonlabelled_images/date=27-03-2024/'
    
    # List objects in the specified folder
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=folder_name)
    
    # Filter image filenames associated with the user_id
    image_filenames = []
    for obj in response.get('Contents', []):
        if user_id in obj['Key']:
            image_filenames.append(obj['Key'])
    
    return image_filenames


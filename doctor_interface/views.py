from django.shortcuts import render
import boto3
import os

def doctor_interface(request):
    image_filenames = []
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        image_filenames = get_user_images_from_s3(user_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        skin_tone = request.POST.get('skin_tone', '')
        melanoma = request.POST.get('melanoma', False)
        

    return render(request, 'doctor_interface.html', {'image_filenames': image_filenames})

def get_user_images_from_s3(user_id):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Specify S3 bucket and folder
    s3_bucket = 'provafinalproject'
    folder_name = 'raw_data/nonlabelled_images/date=27-03-2024/'
    
    # List objects in the specified folder
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=folder_name)
    
    image_filenames = []
    for obj in response.get('Contents', []):
        if user_id in obj['Key']:
            # Download the image temporarily
            temp_file_path = 'doctor_interface/static/temp.jpg'
            s3.download_file(s3_bucket, obj['Key'], temp_file_path)
            
            # Add the temporary file path to the list of image filenames
            image_filenames.append(temp_file_path)
            
    return image_filenames

def delete_temporary_images(image_filenames):
    # Delete temporary image files
    for filename in image_filenames:
        if os.path.exists(filename):
            os.remove(filename)

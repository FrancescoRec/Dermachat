'''this notebook is version 1 of the data pipeline responsible for collecting and preparing 
new images from users that have taken a picture using the app'''

# Importing necessary libraries:
import boto3
from datetime import datetime
import uuid
from .models import ImageMetadata



def upload_user_image(image_data):
    ''' Retreive picture from app request and store it in s3 '''

    # Initialize the S3 client:
    s3 = boto3.client('s3')

    # Declare bucket file variables:
    folder_name = 'raw_data/nonlabelled_images/'


    # Generating a unique filename (We can use any method we prefer while keeping in mind GDPR)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_datetime_for_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user_tag = f'user_{uuid.uuid4()}'
    filename = f"{current_datetime_for_filename}_{user_tag}.jpg"  
    key = folder_name + filename

    # Upload the image data to S3:
    try:
        s3.upload_fileobj(image_data, s3_bucket, key)
        return f"Successfully uploaded image to S3: {key}", user_tag, filename, key, current_datetime
    except Exception as e:
        return f"Error uploading image to S3: {e}"
    
def store_newimage_metadata(user_id, filename, key, timestamp):
    ''' This function stores metadata from the new image to indicate that
    it has not been officially labeled by a specialist after diagnosis'''
    ImageMetadata.objects.create(user_id=user_id, filename=filename, image=key, created_at=timestamp)

    return f"Successfully stored metadata for image: {filename}"


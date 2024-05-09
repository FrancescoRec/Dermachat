'''this notebook is version 1 of the data pipeline responsible for collecting and preparing 
new images from users that have taken a picture using the app'''

# Importing necessary libraries:
import boto3
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv
import uuid

# Load environment variables from .env file
load_dotenv()

def upload_user_image(image_data):
    ''' Retreive picture from app request and store it in s3 '''

    # Initialize the S3 client:
    s3 = boto3.client('s3')

    # Declare bucket file variables:
    folder_name = 'raw_data/nonlabelled_images/date=27-03-2024/'
    s3_bucket = 'provafinalproject'

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
    try:
        # Connect to the PostgreSQL database using environment variables:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        # Create a cursor object to execute SQL queries:
        cursor = connection.cursor()

        # Create a new table named 'new_image_metadata' if it doesn't exist:
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS new_image_metadata (
            user_id VARCHAR (255) PRIMARY KEY,
            filename VARCHAR(255),
            skin_tone VARCHAR(10) DEFAULT 'TBD',
            malignant VARCHAR(10) DEFAULT 'TBD',
            path VARCHAR(255),
            time_taken TIMESTAMP
        )
        '''
        cursor.execute(create_table_query)
        connection.commit()


        # Insert image metadata into the table:
        insert_query = '''
        INSERT INTO new_image_metadata (user_id, filename, skin_tone, malignant, path, time_taken)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (user_id, filename, 'TBD', 'TBD', key, timestamp)) # skin_tone value gets verified by specialist as well
        connection.commit()

        print("Image metadata inserted successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or executing queries:", error)

    finally:
        # Close the cursor and connection:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

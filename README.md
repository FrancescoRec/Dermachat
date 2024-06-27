# DermaChat 🏥 

This is a Django-based web application designed for managing medical images. The app has three main interfaces: one for patients, and two for doctors.

## Project Description

DermaChat facilitates seamless dermatological consultations by allowing patients to upload images and information, which dermatologists can then review and provide feedback on. The app also manages triage lines, ensuring that cases are prioritized and handled appropriately.


## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Models](#models)
- [Interfaces](#interfaces)
- [Credits](#credits)

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

## Environment Variables

This app requires certain environment variables to be set in a `.env` file in the root directory of the project. These include variables for PostgreSQL and AWS.

### Example `.env` file:

```env
# PostgreSQL
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
```

## Usage

1. Run the development server:
    ```bash
    python manage.py runserver
    ```

2. Access the application in your browser at `http://127.0.0.1:8000/`.

## Credits

Olga Beliai: https://github.com/Gliese8
Carlos Varela: https://github.com/CarlosVarelaGreen
Francesco D’aleo: https://github.com/FrancescoRec 
Raphaelle Smyth: https://github.com/rsmythrepo
Jorge Corro: https://github.com/JorgeCCorroV

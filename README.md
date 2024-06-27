# DermaChat 🏥 

### Intro

During the master program, our team has focused on designing, building, and testing a Big Data and A.I. solution for skin cancer detection and optimizing of the melanoma dermatology triage process. Our initial approach involved design thinking techniques to identify a problem that could be addressed using big data and artificial intelligence for healthcare.

Artificial intelligence (AI) has emerged as a transformative technology in healthcare, offering significant potential to enhance diagnostic accuracy, streamline workflows, and optimize patient care. AI's ability to analyze large datasets and identify patterns that may not be readily apparent to human observers positions it as a valuable tool in addressing pressing healthcare challenges, including skin cancer detection and triage optimization.

### Hypothesis
We postulate that the development of a machine learning (ML) model for melanoma classification can automate triage processes for specialists, thereby enhancing efficiency and accuracy in diagnostic procedures. This hypothesis aims to expedite diagnosis for patients requiring immediate attention.

### Solution
In response to this problem, we conceived DermaChat, a platform leveraging AI capabilities for melanoma classification to streamline dermatology triage. By enhancing diagnostic speed and accuracy, DermaChat ensures timely and effective care delivery to high-risk patients while facilitating seamless interaction between patients and dermatology specialists.

DermaChat stands to transform dermatological care delivery, offering a comprehensive solution that empowers both patients and healthcare providers in navigating the complexities of melanoma diagnosis and treatment.
In this segment, we will summarize the process and the solution proposed.

This is a Django-based web application designed for managing medical images. The app has three main interfaces: one for patients, and two for doctors.

## Table of Contents

- [Project Description](#project-description)
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

- Olga Beliai:  https://github.com/Gliese8
- Carlos Varela:  https://github.com/CarlosVarelaGreen
- Francesco D’aleo:  https://github.com/FrancescoRec 
- Raphaelle Smyth:  https://github.com/rsmythrepo
- Jorge Corro:  https://github.com/JorgeCCorroV

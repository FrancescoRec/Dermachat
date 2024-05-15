"""
Django settings for pipino_doctorino project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(t((hg7l&m=&y$*6f*6k@7lw$patq^!3lz7cq-%g$@v9j!bb1^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dermachat",
    "doctor_interface",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pipino_doctorino.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pipino_doctorino.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



import environ

env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Update MEDIA_URL and MEDIA_ROOT for local storage
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

USE_S3=True

# Configure Django storage for Amazon S3
# Assume USE_S3 is defined somewhere in your settings
if USE_S3: 
    # Configure Django storage for Amazon S3
    try:
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        AWS_ACCESS_KEY_ID = 'ASIAXB7FCAWSGL46PBXX'
        AWS_SECRET_ACCESS_KEY = 'RAEFIlb+A1aLojvBnQt4xUNUWNE2RkEilIx8vvoV'
        AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjEEAaCXVzLXdlc3QtMiJIMEYCIQCbTAAziinwhbUB/zo62NuWwOyWKCek9NnpEXBg1eknIgIhAIvrpxYWC116Hzhk8MKDzpJPXV4lij85ORhJYjLV0kd0KrICCKn//////////wEQABoMNDg1Mjc0ODEzODYwIgyvi3Ftjwt+iINO+wkqhgKP5YOFiRSDx5XX6YG1J1Rr36YPrOG5YZaOKNwW/lVq0cdkiVI4M9QgzIa4Vh3maSCnSZGw1yBizFQeAaug9p9WPZuavnzIpY6R9/jAUd2tVjpC3Mk7mOt4wbfMX02p++2zBaLIs+TbqRo1YSCx+b+3eMqc+PEFNR4Uo3TJZhREzV+sr1fMkISCuw0U5gmd9nr9sopDYRTSdex0pNMAmjbES8eijM14bPtI4Janj685x//pkhGRcRROfEgFguZ5ONhZmMWepLMS0oOSu87WGY4xsTMQx7x3QDN+qVUc0lRel+uGcIQnKObe4JBUQo61fG3SbCYTz+gaGD4/8X1w78SRRhrN2UTOMJapk7IGOpwBg8d16tsAEhOOgtiH2EmbQ1spi+SXi2FBN7nkwezGqDBHyYYFDNwNk2stO+jrUQbNxW1rVTOwaADpvM9v3sQZgdoY94jgk515EVlLlqTmvUUVZp0l8fqCtBPp6Lrjyvm12djgAY+yUm5Adb5j569YJ/6sIQeClCXcQFC8C4y9BJUINBRpYm22eZDkUJdVRxNCs8G7jN6BBF80otli'
        AWS_STORAGE_BUCKET_NAME = 'provafinalproject'


    except Exception as e:
        print(f"Error: {e}")
        print("Failed to configure S3 storage. Using local storage instead.")
        USE_S3 = False

if not USE_S3:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




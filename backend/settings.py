"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
environment = os.getenv("DJANGO_ENVIRONMENT", "production")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u6l55vtfp8h0yj04*betj^kh2ow%#pwkmqw#6g6*furkrmq)wx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

if environment == "production":
    CORS_ALLOWED_ORIGINS = [
        "https://wordle-with-friends.up.railway.app"
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        os.getenv("LOCAL_HOST")
    ]

CSRF_TRUSTED_ORIGINS = ['https://wordle-with-friends-backend-production.up.railway.app']

# Application definition

INSTALLED_APPS = [
    'daphne',
    'games',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    

    'rest_framework',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'backend.asgi.application'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (os.environ["REDIS_URL"])
                if environment == "production"
                else ("127.0.0.1", 6379)
            ],
        },
    },
}

# if environment == "production":
#     print('CHANNELS PRODUCTION')
#     CHANNEL_LAYERS["default"] = {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(os.environ["REDIS_URL"])],
#         },
#     }, 

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if environment == "production":
    print('DATABASE PRODUCTION')
    # Use SQLite for development environment
    DATABASES["default"] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["PGDATABASE"],
        'USER': os.environ["PGUSER"],
        'PASSWORD': os.environ["PGPASSWORD"],
        'HOST': os.environ["PGHOST"],
        'PORT': os.environ["PGPORT"],
    }




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

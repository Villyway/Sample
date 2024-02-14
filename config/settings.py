"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta

from django.contrib.messages import constants as messages
from celery.schedules import crontab
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECURE_SSL_REDIRECT = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kr46md$hx%45b*j#o(!0hcxs4u2w0r*1bv5qp^757-#^lsjt%x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External Library
    'rest_framework',
    'import_export',
    'wkhtmltopdf',
    'django_celery_beat',

    # Project applications
    'users.apps.UsersConfig',
    'base.apps.BaseConfig',
    'utils.apps.UtilsConfig',
    'products.apps.ProductsConfig',
    'vendors.apps.VendorsConfig',
    'inventry.apps.InventryConfig',
    # 'inventory.apps.InventoryConfig', 
    'orders.apps.OrdersConfig',
    'customers.apps.CustomersConfig',
    'purchase.apps.PurchaseConfig',
    'dhl_api.apps.DhlApiConfig',
    'inward.apps.InwardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB', 'erp2'), #latestData, inventory1, Asia
        'USER': os.environ.get('DBUSER', 'rupesh'),
        'PASSWORD': os.environ.get('DBPASSWORD', 'Rupesh@123'),
        'HOST': os.environ.get('HOSTURL', 'localhost'),
        'PORT': '5432',
    }
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

TIME_ZONE =  'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(os.path.dirname(
    BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(
    BASE_DIR), "static_cdn", "media_root")

AUTH_USER_MODEL = 'users.User'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/dashboard/'

# Default pagination:
PAGE = 1
PAGE_SIZE = 5

# SMTP Mail setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.hostinger.com'  # 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@basuriautomotive.com'
EMAIL_HOST_PASSWORD = os.environ.get(
    'EMAIL_PASSWORD', 'test@123')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_WELCOME_MESSAGE = "Welcome to  BasuriAutomotive"
DEFAULT_FROM_EMAIL = "info@basuriautomotive.com"

MESSAGE_TAGS = {
    messages.ERROR: 'danger',

}

IMPORT_EXPORT_USE_TRANSACTIONS = True
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000000 # higher than the count of fields

WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': True,
    'margin-top': 10,
    # Add any other options as needed
}
WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf' 

# For redis :
CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', 'redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

CELERY_BEAT_SCHEDULE = {
    'every-mid-night': {
        'task': 'utils.tasks.expir_notification',
        'schedule': crontab(minute=0, hour=0)
    }
}

CORS_ORIGIN_ALLOW_ALL = True

# Rest Framework Contant
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('utils.backends.JWTAuthentication',),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler'
}

# JWT Token life limit
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=45),
}

# Token Key and Algorithm for token
# use settings secret key for JWT secret
JWT_SECRET = os.environ.get('JWT_SECRET', 'ZSWVRSXPBOX12@sd!dsdr5%&*^EGEdgds')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXP_DELTA_SECONDS = 300

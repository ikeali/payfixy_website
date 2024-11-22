"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vw_l1hq2a4!1x=33+kukoonwj1^y7)laf5rgd^ji3(15j*5$+g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'main',
    'kyc'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'website.urls'

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

WSGI_APPLICATION = 'website.wsgi.application'


# CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
'DELETE',
'GET',
'OPTIONS',
'PATCH',
'POST',
'PUT',
]
CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True






# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': config('ENGINE'),
#         'NAME': config('NAME'),
#         'USER': config('USERR'),
#         'PASSWORD': config('PASSWORD'),
#         'HOST': config('HOST'),
#         'PORT': config('PORT'),
#     }
# }



CORS_ALLOWED_ORIGINS = ["http://localhost:3000","http://localhost:3001", "http://localhost:8000","https://payfixy-website-5.onrender.com"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000","http://localhost:3001", "http://localhost:8000", "https://payfixy-website-5.onrender.com"]


if config("ENVIRONMENT") == "DEV":
    DATABASES = {
        'default': {
            'ENGINE': config('ENGINE'),
            'NAME': config('NAME'),
            'USER': config('USERR'),
            'PASSWORD': config('PASSWORD'),
            'HOST': config('HOST'),
            'PORT': config('PORT'),
        }
    }

elif config("ENVIRONMENT") == "STAG":
    DATABASES = {
        'default': dj_database_url.parse(
            config('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }


# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"postgresql://{config('USERR')}:{config('PASSWORD')}@{config('HOST')}:{config('PORT')}/{config('NAME')}",
#         conn_max_age=600
#     )
# }


# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL'),
#         conn_max_age=600  # Optional: Set the connection timeout
#     )
# }


AUTH_USER_MODEL = 'main.User'



# Email configuration
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)  # Default to 587 if not set
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)  # Convert string to boolean
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')





# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# AUTHENTICATION_BACKENDS = [
#     'main.authentication.EmailAuthBackend', 
# ]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of allauth
    'django.contrib.auth.backends.ModelBackend',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

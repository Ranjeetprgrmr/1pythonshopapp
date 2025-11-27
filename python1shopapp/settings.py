
from pathlib import Path
from django.urls import path
from decouple import config
import dj_database_url
import smtplib
from django.core.cache import cache

import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hg2qtq#k_l-%9zcly5m^v1(#0y*my$l5)u0m=_t0_d6c*mxnmh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
# ['.onrender.com', 'localhost', '127.0.0.1']

#Defender Configuration (SQLite only)
DEFENDER_USE_REDIS = False  # Disable Redis completely
DEFENDER_REDIS_URL = ""  # Empty string, not None
DEFENDER_STORE_ACCESS_ATTEMPTS = True  # Use SQLite
DEFENDER_LOCKOUT_TEMPLATE = None  # Default template
DEFENDER_COOLOFF_TIME = 50  # 5 minutes lockout


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
    'axes',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware', 
     'django.contrib.auth.middleware.AuthenticationMiddleware',
    
]


# Session engine (should be default)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]


ROOT_URLCONF = 'python1shopapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'python1shopapp.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

# Database Configuration
# 1. First set a guaranteed valid default
# Database Configuration - REPLACE EVERYTHING
import dj_database_url

# Parse DATABASE_URL and force SSL
# Database Configuration - USE THIS EXACT VERSION
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Parse the database URL manually to ensure SSL is handled
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    # Double ensure SSL is enforced
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Debug output
print(f"Database HOST: {DATABASES['default'].get('HOST')}")
print(f"Database OPTIONS: {DATABASES['default'].get('OPTIONS', {})}")
    
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For production

# CORRECTED - Use a flat list of paths
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Single path as list element
]

# Static files finders (keep this as is)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

AXES_ENABLED = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


# SMTP Configuration
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT' , cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# print(EMAIL_HOST, 'email host')
# print(EMAIL_PORT, 'email port')
# print(EMAIL_HOST_USER, 'email host user')
# print(EMAIL_HOST_PASSWORD, 'email host password')



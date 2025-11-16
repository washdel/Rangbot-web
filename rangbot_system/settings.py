"""
Django settings for rangbot_system project.
"""

from pathlib import Path
import os
from decouple import config

# Database MySQL untuk Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQL_DATABASE', 'rangbot_db'),
        'USER': config('MYSQL_USER', 'rangbot_user'),
        'PASSWORD': config('MYSQL_PASSWORD', 'rangbot_pass'),
        'HOST': config('MYSQL_HOST', 'localhost'),  # 'db' untuk Docker, 'localhost' untuk local
        'PORT': config('MYSQL_PORT', '3306'),
        'CHARSET': 'utf8mb4',
        'INIT_COMMAND': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
}

# Setup pymysql untuk MySQL (jika menggunakan pymysql)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass  # mysqlclient tidak perlu setup ini

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', 'django-insecure-rangbot-development-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # Main app untuk landing page
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

ROOT_URLCONF = 'rangbot_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'rangbot_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Konfigurasi Database
# Default: SQLite (untuk development)
# Untuk menggunakan MySQL, uncomment bagian MySQL dan comment bagian SQLite

# SQLite Configuration (Default) - COMMENTED, Using MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# MySQL Configuration (Laragon)
# Aktifkan MySQL untuk menggunakan database MySQL
try:
    from mysql_config import MYSQL_CONFIG
    DATABASES = {
        'default': MYSQL_CONFIG
    }
    print("✓ Menggunakan MySQL database")
except ImportError:
    print("⚠ mysql_config.py tidak ditemukan, menggunakan SQLite")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
except Exception as e:
    print(f"⚠ Error loading MySQL config: {e}, menggunakan SQLite")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'id-id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


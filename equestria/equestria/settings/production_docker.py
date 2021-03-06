"""
Django settings for equestria project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from equestria.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "staging.equestria.cls.ru.nl",
    "equestria.cls.ru.nl",
    "equestria.larsvanrhijn.nl",
    "clst.giphouse.nl",
]

SESSION_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/equestria/log/django.log",
        },
    },
    "loggers": {
        "": {"handlers": ["file"], "level": "DEBUG", "propagate": True,},
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    }
}

if os.environ.get("ADMIN_EMAIL"):
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

if os.environ.get("TEMP_FOLDER"):
    TMP_DIR = os.environ.get("TEMP_FOLDER")

if os.environ.get("DOWNLOAD_FOLDER"):
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_FOLDER")

if os.environ.get("USER_FOLDER"):
    USER_DATA_FOLDER = os.environ.get("USER_FOLDER")

if os.environ.get("PROCESS_DATA_FOLDER"):
    PROCESS_DATA_FOLDER = os.environ.get("PROCESS_DATA_FOLDER")

if not os.path.exists(os.path.join(MEDIA_ROOT, USER_DATA_FOLDER)):
    os.makedirs(os.path.join(MEDIA_ROOT, USER_DATA_FOLDER))

if not os.path.exists(os.path.join(MEDIA_ROOT, PROCESS_DATA_FOLDER)):
    os.makedirs(os.path.join(MEDIA_ROOT, PROCESS_DATA_FOLDER))

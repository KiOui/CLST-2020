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
]

SESSION_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.environ.get("DJANGO_LOG_FILE"),
        },
    },
    "loggers": {
        "": {"handlers": ["file"], "level": "DEBUG", "propagate": True,},
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DATABASE_LOCATION"),
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


if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

if not os.path.exists(USER_DATA_FOLDER):
    os.makedirs(USER_DATA_FOLDER)

"""
Django settings for equestria project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from equestria.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "20!5%%x%+4j1un2v1p^cz!ld2fx00+jd!%!3%ax^d&mk4pl9w#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
X_FRAME_OPTIONS = "SAMEORIGIN"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler",},
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO", "propagate": True,},
    },
}


ROOT_URLCONF = "equestria.urls"


if not os.path.exists(os.path.join(MEDIA_ROOT, USER_DATA_FOLDER)):
    os.makedirs(os.path.join(MEDIA_ROOT, USER_DATA_FOLDER))

if not os.path.exists(os.path.join(MEDIA_ROOT, PROCESS_DATA_FOLDER)):
    os.makedirs(os.path.join(MEDIA_ROOT, PROCESS_DATA_FOLDER))

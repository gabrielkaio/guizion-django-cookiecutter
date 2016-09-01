from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{local_database_name}}',
        'USER': '{{local_database_user}}',
        'PASSWORD': '{{local_database_password}}',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

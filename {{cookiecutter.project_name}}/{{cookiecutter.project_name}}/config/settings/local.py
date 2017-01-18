from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{cookiecutter.local_database_name}}',
        'USER': '{{cookiecutter.local_database_user}}',
        'PASSWORD': '{{cookiecutter.local_database_password}}',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

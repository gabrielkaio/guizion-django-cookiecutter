from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{cookiecutter.production_database_name}}',
        'USER': '{{cookiecutter.production_database_user}}',
        'PASSWORD': '{{cookiecutter.production_database_password}}',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

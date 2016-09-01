from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{production_database_name}}',
        'USER': '{{production_database_user}}',
        'PASSWORD': '{{production_database_password}}',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

"""
Django settings.
"""
import environ
import os

BASE_DIR = environ.Path(__file__) - 3
APPS_DIR = BASE_DIR.path('{{ cookiecutter.project_name }}')

env = environ.Env()
env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xr$vhads4iz7xl(nj-=-8zgl3g#v)ow2b*o&nvrn+c-q7djmf+'

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'oauth2_provider',
    's3direct',
)

LOCAL_APPS = (
    '{{cookiecutter.project_name}}.apps.accounts'
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'accounts.User'

ROOT_URLCONF = '{{cookiecutter.project_name}}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ]
        ,
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

WSGI_APPLICATION = '{{cookiecutter.project_name}}.wsgi.application'

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEVICE_TOKEN_HEADER = "HTTP_DEVICE_TOKEN"
DEVICE_AGENT_HEADER = "HTTP_DEVICE_AGENT"
DEVICE_LANGUAGE_HEADER = "HTTP_DEVICE_LANGUAGE"

# Celery Conf
BROKER_URL = 'amqp://{{cookiecutter.rabbitmq_user}}:{{cookiecutter.rabbitmq_password}}@localhost:5672/{{cookiecutter.rabbitmq_app}}'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_ENABLE_UTC = True

# Static and Media files (CSS, JavaScript, Images)
STATIC_ROOT = str(BASE_DIR('static'))

STATIC_URL = '/static/'

MEDIA_ROOT = str(BASE_DIR('media'))

MEDIA_URL = '/media/'

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 16070400,  # 180 day, approximately 6 months
    'OAUTH2_VALIDATOR_CLASS': "{{cookiecutter.project_name}}.apps.utils.oauth_extension.OAuthLibExtension",
    'OAUTH2_BACKEND_CLASS': "{{cookiecutter.project_name}}.apps.utils.oauth_extension.OAuthLibCoreExtension",
}


def create_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('img', filename)


S3DIRECT_DESTINATIONS = {
    'categories': (create_filename, lambda u: True, ['image/jpeg', 'image/png', 'image/gif']),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
    'COMPACT_JSON': True,
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

AWS_STORAGE_BUCKET_NAME = '{{cookiecutter.s3_bucket_name}}'

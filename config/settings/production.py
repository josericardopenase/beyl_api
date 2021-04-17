from .base import *

DEBUG = config('DEBUG', False)

ASGI_APPLICATION = "config.asgi.application"


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]

}

THIRD_PARTY_APPS += [

    'storages',
    's3_folder_storage',
    'anymail',

]


ALLOWED_HOSTS = ['beyl-api.herokuapp.com', '127.0.0.1', 'localhost', 'beylapp.com', 'api.beylapp.com']
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#STATIC AND MEDIA FILES

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"config/static")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_ACCESS_KEY_ID        = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_BUCKET_NAME')

AWS_S3_REGION_NAME="eu-west-1"
AWS_S3_HOST = "s3.eu-west-1.amazonaws.com"

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

import dj_database_url

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
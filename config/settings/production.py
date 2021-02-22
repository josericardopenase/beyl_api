from .base import *

DEBUG = False

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
    'anymail'

]


ALLOWED_HOSTS = ['https://beyl-api.herokuapp.com/', 'http://127.0.0.1:8000/']
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#STATIC AND MEDIA FILES


STATIC_URL = '/api/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"config/static")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_ACCESS_KEY_ID        = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_BUCKET_NAME')

AWS_S3_REGION_NAME="eu-west-2"
AWS_S3_HOST = "s3.eu-west-2.amazonaws.com"

""" STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage' """
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_S3_PATH = 'static/'



#CONNECTIONS CONFIGURATION

import dj_database_url

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500
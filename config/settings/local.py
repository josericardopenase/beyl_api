from .base import *

DEBUG = True

THIRD_PARTY_APPS += [

    'storages',
    's3_folder_storage',
    'anymail',
    'ckeditor',

]


ALLOWED_HOSTS = ['*',]
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


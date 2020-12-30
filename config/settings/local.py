from .base import *


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")

]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static_root")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media', 'media_root')
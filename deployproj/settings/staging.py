from deployproj.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'rapidsms'

INSTALLED_APPS += (
    'gunicorn',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_SUBJECT_PREFIX = '[Deployproj Staging] '

COMPRESS_ENABLED = True

# ALLOWED_HOSTS needs to be set or Django will 500.
# But our nginx config rejects bad hosts in requests, so we can just
# wildcard this for Django.
ALLOWED_HOSTS = ['*']

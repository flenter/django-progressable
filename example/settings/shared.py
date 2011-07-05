import sys

globals().update(vars(sys.modules['settings']))

import os

SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

ADMINS += (
    )

TIME_ZONE = 'Europe/Amsterdam'

# Static media location (for instance the admin media)
STATIC_ROOT = os.path.join(SITE_ROOT, 'collected_media')

STATIC_URL = '/collected_media/'


# Dynamic media location (i.e. files that have been uploaded by users or belong to this site only)
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

TEMPLATE_DIRS += (
    os.path.join(SITE_ROOT, 'customcore', 'templates'),
    os.path.join(SITE_ROOT, 'core', 'templates'),
    os.path.join(SITE_ROOT, 'progressable', 'templates'),
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    
    )\
    + INSTALLED_APPS + (
    
    'django.contrib.admin',
    'django.contrib.sitemaps', 
    'django.contrib.staticfiles',
    
    'sentry',
    'sentry.client',
    'django_extensions',
    'south',
    'reversion',
    'djcelery',
#    'piston',
#    'sitetree',
#    'djutils',
#    'staticgenerator',
    'tastypie',
    'core',
    'progressable',
#    'customcore',
)

import sys

STATICFILES_DIRS = (
    os.path.realpath(
        os.path.join(
            SITE_ROOT,
            '..',
            'lib',
            'python%d.%d' %
            (
                sys.version_info[0],
                sys.version_info[1]
            ),
            'site-packages',
            'admin_tools',
            'media'
        )
    ),
)

SERVER_EMAIL = 'no-reply@secretcodemachine.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

QUEUE_CLASS = 'djutils.queue.backends.database.DatabaseQueue'
QUEUE_CONNECTION = ''

WEB_ROOT = os.path.join(SITE_ROOT, 'temp', 'export')

import logging

from sentry.client.handlers import SentryHandler
logger = logging.getLogger()

CACHES = {
    'default': {
      'BACKEND': 'redis_cache.RedisCache',
      'LOCATION': '127.0.0.1:6379',
      'OPTIONS': {
        'DB': 2,
        'PASSWORD':'',
        },
      },
    }

SESSION_ENGINE = 'redis_sessions.backends.redis'

ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

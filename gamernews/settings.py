import os
import sys
import platform
import djcelery

djcelery.setup_loader()

from django.contrib.messages import constants as messages

# ===========================
# = Directory Declaractions =
# ===========================

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR   = os.path.dirname(__file__)
TEMPLATE_DIRS = (os.path.join(CURRENT_DIR, 'templates'),)
MEDIA_ROOT    = os.path.join(CURRENT_DIR, 'media/')
UTILS_ROOT    = os.path.join(CURRENT_DIR, 'utils')
VENDOR_ROOT    = os.path.join(CURRENT_DIR, 'vendor')

if '/utils' not in ' '.join(sys.path):
    sys.path.append(UTILS_ROOT)

if '/vendor' not in ' '.join(sys.path):
    sys.path.append(VENDOR_ROOT)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Tyler Rilling', 'tyler@underlost.net'))
MANAGERS = ADMINS

ALLOWED_HOSTS = ['news.underlost.com', 'news.underlost.net', 'news.underlost.org', 'gamernews.herokuapp.com']

#DB info injected by Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

import urlparse
redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
        'default': {
        'BACKEND': 'gamernews.vendor.johnny.backends.redis.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
        'PASSWORD': redis_url.password,
        'DB': 0,
        'JOHNNY_CACHE': True,
    }
  }
}

JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_gnews'
JOHNNY_MIDDLEWARE_SECONDS = 900
JOHNNY_TABLE_WHITELIST = ['news.Blob',]

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
# Set to False to disable people from creating new accounts.
ALLOW_NEW_REGISTRATIONS = True

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = "25"
#EMAIL_USE_TLS = True

#Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'static.news.underlost.net'
AWS_S3_CUSTOM_DOMAIN = 'static.news.underlost.com'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False
COMPRESS_URL = "http://static.news.underlost.net/"
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Set to False to disable people from creating new accounts.
ALLOW_NEW_REGISTRATIONS = True
SITE_NAME = 'Gamer News'
SITE_DESC = 'Video Game News'
SITE_URL = 'http://news.underlost.net/'
COMMENTS_APP = 'gamernews.apps.threadedcomments'

TIME_ZONE = 'GMT'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
AUTH_USER_MODEL = 'core.Account'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = (os.path.join(SITE_ROOT, 'static'),)
WSGI_APPLICATION = 'gamernews.wsgi.application'

if DEBUG:
	STATIC_ROOT = os.path.join(CURRENT_DIR, 'static')
	STATIC_URL = 'http://direct.news.underlost.net/static/'
else:
	STATIC_ROOT = 'staticfiles'
	STATIC_URL = 'http://static.news.underlost.net/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'gamernews.vendor.johnny.middleware.LocalStoreClearMiddleware',
	'gamernews.vendor.johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'gamernews.apps.core.middleware.TimingMiddleware',
    'gamernews.apps.core.middleware.LastSeenMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = {	
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.tz',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'gamernews.apps.core.context_processors.template_settings',
}

ROOT_URLCONF = 'gamernews.urls'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
	#Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    
    #Prancing on Heroku
    'djcelery',
    'gunicorn',
    'taggit',
    'compressor',
    'storages',
    
    #vendor
    'gamernews.vendor.django_comments',
    
    #Internal
    'gamernews.apps.core',
    'gamernews.apps.news',
    'gamernews.apps.voting',
    'gamernews.apps.threadedcomments',
)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/u/%s/" % u.username,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

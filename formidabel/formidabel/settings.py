# -*- coding: utf-8 -*-
import os
import sys

gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# To find DwcA (TODO: move to proper python dependency)
sys.path.insert(0, os.path.join(PROJECT_PATH, 'lib/dwca'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "../static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'formidabel.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'formidabel.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',

    'django.contrib.markup',
    'cmsplugin_markdown',

    'ants_atlas',

    'tastypie',
    'backbone_tastypie',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

TEMPLATE_DIRS = (
    # The docs say it should be absolute path: PROJECT_PATH is precisely one.
    # Life is wonderful!
    os.path.join(PROJECT_PATH, "templates"),
)

CMS_TEMPLATES = (
    ('standard_page.html', 'Standard page'),
)

LANGUAGES = [
    ('en', 'English'),
]

# Let's set up a few things for easy Heroku deployment
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# (from Heroku doc)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Ants Atlas configuration:

# Map (WMS) available overlays
ANTSATLAS_CONFIG = {
    'map_overlays': {

        'Phytoregions': {
            'url': 'http://gis.bebif.be:80/geoserver2/wms',
            'layers': 'bbpf:Regions_Phyto_Clipped'},
        'Broad-leaved forest': {
            'url': 'http://gis.bebif.be:80/geoserver2/wms',
            'layers': 'eea:mergedandclipped',
            'cql_filter': 'CODE_00=311',
            'styles': 'CORINE_DISTINCT_FOREST'},
        'Coniferous forest': {
            'url': 'http://gis.bebif.be:80/geoserver2/wms',
            'layers': 'eea:mergedandclipped',
            'cql_filter': 'CODE_00=312',
            'styles': 'CORINE_DISTINCT_FOREST'},
        'Mixed forest': {
            'url': 'http://gis.bebif.be:80/geoserver2/wms',
            'layers': 'eea:mergedandclipped',
            'cql_filter': 'CODE_00=313',
            'styles': 'CORINE_DISTINCT_FOREST'},
    },
}


# {
#                         'Phytoregions': L.tileLayer.wms("http://gis.bebif.be:80/geoserver2/wms", {
#                             layers: 'bbpf:Regions_Phyto_Clipped',
#                             format: 'image/png',
#                             transparent: true 
#                         }),
#                         'Broad-leaved forest': L.tileLayer.wms("http://gis.bebif.be:80/geoserver2/wms", {
#                             layers: 'eea:mergedandclipped',
#                             format: 'image/png',
#                             transparent: true,
#                             cql_filter: 'CODE_00=311',
#                             styles: 'CORINE_DISTINCT_FOREST'
#                         }),
#                         'Coniferous forest': L.tileLayer.wms("http://gis.bebif.be:80/geoserver2/wms", {
#                             layers: 'eea:mergedandclipped',
#                             format: 'image/png',
#                             transparent: true,
#                             cql_filter: 'CODE_00=312',
#                             styles: 'CORINE_DISTINCT_FOREST'
#                         }),
#                         'Mixed forest': L.tileLayer.wms("http://gis.bebif.be:80/geoserver2/wms", {
#                             layers: 'eea:mergedandclipped',
#                             format: 'image/png',
#                             transparent: true,
#                             cql_filter: 'CODE_00=313',
#                             styles: 'CORINE_DISTINCT_FOREST'
#                         })
#                     }


try:
    from localsettings import *
except ImportError:
    pass

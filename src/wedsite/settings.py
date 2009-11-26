# Django settings for wedsite project.
import os
import socket

ROOT_URLCONF = 'wedsite.urls'
ROOTDIR = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')

LOGIN_URL='/login/'

DEV_MACHINE = socket.gethostname() == 'SYSADMIN'

DEBUG = True and DEV_MACHINE

DATABASE_ENGINE = 'sqlite3'                 # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ROOTDIR + '/wedsite.db'     # Or path to database file if using sqlite3.
DATABASE_USER = ''                          # Not used with sqlite3.
DATABASE_PASSWORD = ''                      # Not used with sqlite3.
DATABASE_HOST = ''                          # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                          # Set to empty string for default. Not used with sqlite3.

TEMPLATE_DEBUG = DEBUG

ADMINS = (
          ('gabriele', 'gabriele.ctn@gmail.com'),
          ('cecilia', ''),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Andorra'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-it'

gettext = lambda s: s

LANGUAGES = (
    ('it', gettext('Italian')),
    ('en', gettext('English')),
)
DEFAULT_LANGUAGE = 0

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r#1x-+z02r$_eim4(s26-l*41hh(xx08^g9l&afg+kx$_fzclb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.auth',
    'multilingual.context_processors.multilingual',
    'wedsite.nav.context_processors.mainnav',
    'wedsite.nav.context_processors.subnav',
    'wedsite.feeds.context_processors.feed_url',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'signedcookies.middleware.SignedCookiesMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'multilingual.middleware.DefaultLanguageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOTDIR + '/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    #'django.contrib.flatpages',
    #'signedcookies',
    'multilingual',
    #'multilingual.flatpages',
    'wedsite',
    'wedsite.ipsecurity',
    'wedsite.nav',
    'wedsite.feeds',
    'wedsite.news',
    'wedsite.polls',
    'wedsite.confirm',
)
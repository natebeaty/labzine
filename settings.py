# Django settings for labzine project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Nate Beaty', 'nate@clixel.com'),
)

MANAGERS = (
    ('Nate Beaty', 'nate@clixel.com'),
    ('Joseph Robertson', 'josepherobertson@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'natebeaty_lab',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'joseph@lab-zine.com'
SERVER_EMAIL = 'joseph@lab-zine.com'

SITE_URL = 'lab-zine.com'
# SERVER_EMAIL = 'www@%s' % SITE_URL

# Extend cookie age to a year
SESSION_COOKIE_AGE = 31104000

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Etc/GMT+8'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 2

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_ROOT = '/var/www/labzine/media/'
# MEDIA_ROOT = '/home/natebeaty/django/django_projects/labzine/media/'
# MEDIA_ROOT = '/home/natron46/django_projects/labzine/media/'
# MEDIA_ROOT = '/home/natebeaty/domains/lab-zine.com/web/public/media/'
MEDIA_ROOT = '/home/natebeaty/webapps/labzine_static/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'labzine.middleware.threadlocals.ThreadLocals', 
    # 'djangologging.middleware.LoggingMiddleware',
)

ROOT_URLCONF = 'labzine.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    # '/Users/natebeaty/django/django_templates',
    # '/Users/natebeaty/django/django_projects/pdxguide/templates',
    # '/home/natebeaty/django/django_templates',
    # '/home/natebeaty/django/django_projects/labzine/templates',
    # '/home/natron46/django_templates',
    '/home/natebeaty/webapps/django/labzine/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "labzine.articles.context_processors.lab_issues",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'labzine.tagsfield',
    'labzine.articles',
    'labzine.blog',
    # 'django.contrib.comments',
)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'cache',
#     }
# }

# CACHE_BACKEND = 'db://cache'
# CACHE_MIDDLEWARE_SECONDS = 86400
# CACHE_MIDDLEWARE_KEY_PREFIX = 'labzine'

# Custom global variables
YAHOO_ID = ''

# INTERNAL_IPS = ()

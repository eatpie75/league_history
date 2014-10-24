from datetime import timedelta
import os.path

PROJECT_DIR=os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE':	'django.db.backends.postgresql_psycopg2',
		'HOST':		'localhost',
		'NAME':		'lol',
		'USER':		'django',
		'PASSWORD':	'ohsocool',
		'CONN_MAX_AGE': 300,
	}
}

SOUTH_DATABASE_ADAPTERS = {
	'default': 'south.db.postgresql_psycopg2'
}

CACHES = {
	'default': {
		'BACKEND':	'redis_cache.cache.RedisCache',
		'LOCATION':	'127.0.0.1:6379:0',
		'TIMEOUT':	0,
		'OPTIONS': {
			'PICKLE_VERSION':2
		}
	}
}

BROKER_URL="redis://localhost:6379/1"
CELERY_RESULT_BACKEND="redis://localhost:6379/2"
CELERYD_CONCURRENCY=1
CELERY_TASK_RESULT_EXPIRES=timedelta(minutes=30)
CELERYBEAT_SCHEDULE = {
	"auto_update": {
		"task": "lol.tasks.auto_update",
		"schedule": timedelta(minutes=10),
	},
	"auto_fill": {
		"task": "lol.tasks.auto_fill",
		"schedule": timedelta(minutes=11),
	},
	"challenger_fill": {
		"task": "lol.tasks.challenger_fill",
		"schedule": timedelta(minutes=23),
	},
	"check_all_servers": {
		"task": "lol.tasks.check_servers",
		"schedule": timedelta(minutes=2),
	},
}
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z6oyhza0dob#eue&amp;*2*_nsx79_-xa#3-05sitokb(l-07^pvuc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django_jinja.loaders.AppLoader',
	'django_jinja.loaders.FileSystemLoader',
)

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.html.j2'
JINJA2_ENVIRONMENT_OPTIONS = {
	'autoescape': True
}
MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	# 'django.middleware.transaction.TransactionMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS=(
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.tz",
	"django.contrib.messages.context_processors.messages",
	"lol.context_processors.ajax_base",
	"lol.context_processors.game_types"
)

ROOT_URLCONF = 'unknown.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'unknown.wsgi.application'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	# os.path.join(PROJECT_DIR, 'unknown', 'templates'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	# 'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
	'djcelery',
	'django_jinja',
	'lol',
)

try:
	from settings_local import *
except ImportError:
	pass

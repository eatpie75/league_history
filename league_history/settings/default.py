# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = ('127.0.0.1',)
INTERNAL_IPS = ('127.0.0.1',)

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 'easy_thumbnails',
	'djcelery',
	'django_jinja',
	'lol'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'league_history.urls'
WSGI_APPLICATION = 'league_history.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATES = [
	{
		"BACKEND": "django_jinja.backend.Jinja2",
		"APP_DIRS": True,
		"OPTIONS": {
			"constants":{},
			"context_processors": [
				"django.contrib.auth.context_processors.auth",
				"django.template.context_processors.debug",
				"django.template.context_processors.i18n",
				"django.template.context_processors.media",
				"django.template.context_processors.static",
				"django.template.context_processors.tz",
				"django.contrib.messages.context_processors.messages",
				"lol.context_processors.ajax_base",
				"lol.context_processors.game_types"
			],
		}
	},
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.contrib.auth.context_processors.auth",
				"django.template.context_processors.debug",
				"django.template.context_processors.i18n",
				"django.template.context_processors.media",
				"django.template.context_processors.static",
				"django.template.context_processors.tz",
				"django.contrib.messages.context_processors.messages",
				"lol.context_processors.ajax_base",
				"lol.context_processors.game_types"
			],
		}
	},
]

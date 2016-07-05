# minent.settings.base
# The common Django settings for the minent project.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 14:10:54 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
The common Django settings for the minent project.

This file was adapated by the settings.py file generated by
'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os
import dj_database_url


##########################################################################
## Helper function for environmental settings
##########################################################################

def environ_setting(name, default=None):
    """
    Fetch setting from the environment- if not found, then this setting is
    ImproperlyConfigured.
    """
    if name not in os.environ and default is None:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "The {0} ENVVAR is not set.".format(name)
        )

    return os.environ.get(name, default)


##########################################################################
## Build Paths inside of project with os.path.join
##########################################################################

## Project is the location of the minent directory (with the wsgi.py)
## Note that BASE_DIR (originally in this file) is the same as Project
## Repository is the location of the project and the apps and other files
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY = os.path.dirname(PROJECT)


##########################################################################
## Secret settings - do not store!
##########################################################################

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ_setting("SECRET_KEY")

##########################################################################
## Database Settings
##########################################################################

## See" https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(),
}

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

##########################################################################
## Runtime settings
##########################################################################

## Debugging settings
## SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

## Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

## Hosts - specify in production settings
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ('127.0.0.1',)

## WSGI Configuration
ROOT_URLCONF = 'minent.urls'
WSGI_APPLICATION = 'minent.wsgi.application'

## Application definition
INSTALLED_APPS = [
    # Django apps
    'grappelli', # Must come before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'social.apps.django_app.default',
    'rest_framework',

    # Minimum Entropy apps
]

## Request Handling
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
]

## Internationalization
## https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

## Admin Title
GRAPPELLI_ADMIN_TITLE = "Minimum Entropy Admin"

##########################################################################
## Content (Static, Media, Templates)
##########################################################################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/assets/'

STATICFILES_DIRS = (
    os.path.join(PROJECT, 'assets'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

## Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

##########################################################################
## Authentication
##########################################################################

## Password validation
## https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

## Support for Social Auth authentication backends
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

## Social authentication strategy
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

## Google-specific authentication keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = environ_setting("GOOGLE_OAUTH2_CLIENT_ID", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ_setting("GOOGLE_OAUTH2_CLIENT_SECRET", "")

LOGIN_REDIRECT_URL = "home"

## Error handling
SOCIAL_AUTH_LOGIN_ERROR_URL = "login"
SOCIAL_AUTH_GOOGLE_OAUTH2_SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'bbengfort@districtdatalabs.com'),
    ('Tony Ojeda', 'tojeda@districtdatalabs.com'),
    ('Rebecca Bilbro', 'rbilbro@districtdatalabs.com'),
)

SERVER_EMAIL    = 'DDL Admin <admin@districtdatalabs.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER      = environ_setting("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD  = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587
EMAIL_SUBJECT_PREFIX = '[MINENT] '

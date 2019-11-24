"""
Django settings for hknweb project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os
from django.conf.global_settings import DATETIME_INPUT_FORMATS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
# Application definition

INSTALLED_APPS = [
    'hknweb',
    'hknweb.events',
    'hknweb.tutoring',
    'hknweb.markdown_pages',
    'hknweb.shortlinks',
    'hknweb.alumni',
    'hknweb.candidate',
    'hknweb.elections',
    'hknweb.courses',
    'hknweb.exams',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markdownx',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hknweb.urls'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'hknweb.views.users.add_officer_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'hknweb.wsgi.application'

AUTHENTICATION_BACKENDS = (
 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
 'social_core.backends.google.GoogleOpenId',  # for Google authentication
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication

 'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hknweb',
        'HOST': 'mysql',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'read_default_file': "~/.my.cnf",
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

DATETIME_INPUT_FORMATS += ('%m/%d/%Y %I:%M %p')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# File uploads

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email stuff

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'smtp.gmail.com'

# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'hknwebsite@hkn.eecs.berkeley.edu'
EMAIL_USE_TLS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'hknweb', 'static'),
]

# placeholder for now, replace with home page when it exists
LOGIN_URL = 'accounts/login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['hkn.eecs.berkeley.edu']

# Recaptcha: public and private key
RECAPTCHA_PUBLIC_KEY = '6LeYTKAUAAAAADooVC_FG9ua47PnwP_gGWOSwauK'

# python-social-auth: MySQL InnoDB index limits
# https://python-social-auth-docs.readthedocs.io/en/latest/configuration/settings.html#tweaking-some-fields-length
SOCIAL_AUTH_UID_LENGTH = 223
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 100
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH  = 100

# Constants for backend code

# user groups
CAND_GROUP = 'candidate'
OFFICER_GROUP = 'officer'

# default hard-coded event types for candidate semester
# NOTE: these strings are also hard-coded in candidate/index.html
MANDATORY_EVENT = 'mandatory'
FUN_EVENT = 'fun'
BIG_FUN_EVENT = 'big_fun'
SERV_EVENT = 'serv'
PRODEV_EVENT = 'prodev'
HANGOUT_EVENT = 'hangout'

# Note: both candidate and officer group should have permission to add officer challenges

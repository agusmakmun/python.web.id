"""
Django 2.0.2.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'key-key-key-key'

SITE_ID = 1
DEBUG = True
PAGINATE_BY = 10
TAGS_PAGINATE_BY = 500
ADMIN_LIST_PER_PAGE = 20
ALLOWED_HOSTS = ['*']

# Email Settings
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FILE_UPLOAD_MAX_MEMORY_SIZE = 35000000

# Production mode
if not DEBUG:
    # activate the logging
    from djangoblog.utils.logger import LOGGING
    LOGGING = LOGGING

    # to enable / disable `HTML Minify` middleware
    HTML_MINIFY = True

    # to enable send an email for logging errors
    SERVER_EMAIL = EMAIL_HOST_USER
    ADMINS = [('Your Name', EMAIL_HOST_USER), ]
    MANAGERS = ADMINS

# No Recaptha SITE_KEY and SECRET KEY
NORECAPTCHA_SITE_KEY = "key-key-key-key"
NORECAPTCHA_SECRET_KEY = "key-key-key-key"

# Disqus API Key
DISQUS_API_KEY = 'key-key-key-key'
DISQUS_WEBSITE_SHORTNAME = 'website-short-name'

# Rest API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'app_blog.utils.paginator.StandardRestAPIPagination',
    'PAGE_SIZE': 100,
}

# Martor (Markdown Editor)
MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',
    'mention': 'true',
    'jquery': 'true',
}
MARTOR_IMGUR_CLIENT_ID = 'key-key-key-key'
MARTOR_IMGUR_API_KEY = 'key-key-key-key'
MARTOR_MARKDOWN_BASE_MENTION_URL = '/posts/author/'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sitemaps',
    'django.contrib.sites',

    # 3d party apps
    'djipsum',  # for development mode, to create a dummy
    'updown',
    'martor',
    'disqus',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.linkedin',
    'rest_framework',
    'rest_framework.authtoken',  # please migrate first

    # major aps
    'app_api',
    'app_blog',
    'app_user',
    'app_dashboard',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Auth and allauth settings
# ACCOUNT_SIGNUP_FORM_CLASS = 'app_user.forms.SignUpForm'
ACCOUNT_FORMS = {
    'signup': 'app_user.forms.SignUpForm',
    'login': 'app_user.forms.LoginForm',
    'reset_password': 'app_user.forms.ResetPasswordForm'
}
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user:email', ]
    },
    'linkedin': {
        'SCOPE': ['r_emailaddress'],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url'
        ]
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 3D Party APPS
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

    # Custom middleware
    'django.middleware.locale.LocaleMiddleware',
    # 'djangoblog.utils.middleware.LanguageMiddleware',
    # 'djangoblog.utils.middleware.OnlineNowMiddleware',
]

ROOT_URLCONF = 'djangoblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Enable {{ STATIC_URL }} and {{ MEDIA_URL }}
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoblog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    }
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
LANGUAGES = (
    ('en', 'English'),
    ('id', 'Indonesia')
)
DEFAULT_LANGUAGE = 1
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    '/path/to/env-djangoblog/djangoblog/static',
)

STATIC_URL = '/static/'
#STATIC_ROOT = '/path/to/env-djangoblog/djangoblog/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/path/to/env-djangoblog/djangoblog/media'

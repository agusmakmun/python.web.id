"""
Django 3.1.1
"""

from pathlib import Path


SITE_ID = 1
DEBUG = True
ALLOWED_HOSTS = ['*']
DEFAULT_PAGINATION_NUMBER = 10
SECRET_KEY = 'xxxx-xxxx-xxxx-xxxx'
BASE_DIR = Path(__file__).resolve().parent.parent


# Google TLS Configuration for port 587
# 1. Unlock Captha: https://accounts.google.com/DisplayUnlockCaptcha
# 2. Change to active: https://www.google.com/settings/security/lesssecureapps
# 3. Go to the 2-Step Verification: https://myaccount.google.com/signinoptions/two-step-verification/enroll-welcome
# 4. Create app password: https://security.google.com/settings/security/apppasswords
# 5. Use that password into 'EMAIL_HOST_PASSWORD'
# Other: https://admin.google.com/AdminHome#SecuritySettings: => Basic Settings => Less Secure Apps => select option: 2
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'xxxx@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FILE_UPLOAD_MAX_MEMORY_SIZE = 35000000


# Martor Configuration
MARTOR_THEME = 'bootstrap'  # "semantic"
MARTOR_IMGUR_CLIENT_ID = 'xxxx'
MARTOR_IMGUR_API_KEY = 'xxxx'
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'true',        # to enable/disable imgur/custom uploader.
    'mention': 'false',     # to enable/disable mention
    'jquery': 'true',       # to include/revoke jquery (require for admin default django)
    'living': 'false',      # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}


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
    'captcha',
    'martor',
    'updown',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.linkedin',

    # major apps
    'apps.accounts',
    'apps.blog',
    'apps.product',
]


MIDDLEWARE = [
    # custom middleware
    'corsheaders.middleware.CorsMiddleware',

    # default middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates/allauth',
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Cache
# https://docs.djangoproject.com/en/3.1/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Custom Auth User Model
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    # custom auth backend
    'apps.accounts.utils.backends.CustomAuthBackend'
]


# Auth and allauth settings
ACCOUNT_FORMS = {
    'signup': 'apps.accounts.forms.auth.SignUpForm',
    'login': 'apps.accounts.forms.auth.LoginForm',
    'reset_password': 'apps.accounts.forms.auth.ResetPasswordForm'
}


EMAIL_REQUIRED = True  # allauth
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


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGES = (
    ('en', 'English'),
    ('id', 'Indonesia')
)
DEFAULT_LANGUAGE = 1
LOCALE_PATHS = (
    BASE_DIR / 'locale',
    BASE_DIR / 'locale/rest_auth',
)
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True


# handle in computer machine, not in this django app
# sudo timedatectl set-timezone Asia/Jakarta
# https://python.web.id/posts/detail/how-to-handle-timezone-localtime-in-django/
TIME_ZONE = 'Asia/Jakarta'
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# If you want to run `./manage.py collectstatic`, please following this:
# 1. un-comment `STATIC_ROOT` and comment `STATICFILE_DIRS`
# 2. If you already done, then:
# 3. un-comment `STATICFILE_DIRS` and comment again `STATIC_ROOT`
STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'static', ]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Google re-captcha (from apps.configs)
# https://www.google.com/u/6/recaptcha/admin/site/347092627/settings
RECAPTCHA_PUBLIC_KEY = 'xxxx-xxxx'
RECAPTCHA_PRIVATE_KEY = 'xxxx-xxxx'


# Django Cors Header
# Only enable CORS for specified domains
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'accept-language',
    'authorization',
    'authorization-uploader',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with'
)

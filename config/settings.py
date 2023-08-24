from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1',]

# Add here your deployment HOSTS
CSRF_TRUSTED_ORIGINS = ['http://localhost']


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # local
    "customAdmin.apps.CustomadminConfig",
    "accounts.apps.AccountsConfig",
    "bizxross.apps.BizxrossConfig",
    "employee.apps.EmployeeConfig",
    "employer.apps.EmployerConfig",
    "job.apps.JobConfig",
    "proposal.apps.ProposalConfig",
    "message.apps.MessageConfig",
    "tailwindcss.apps.TailwindcssConfig",
    # 3rd-party
    "compressor",
    "allauth",
    "allauth.account",
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.notification.NotificationMiddleware"
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER':  os.getenv("DB_USER"),
        'PASSWORD':  os.getenv("DB_PASSWORD"),
        'HOST':'localhost',
        'PORT':'3307',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Authentication User Model
AUTH_USER_MODEL = "accounts.User"

# Internationalization
LANGUAGE_CODE = "ja-jp"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = "static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)

MEDIA_URL = "/media/"
MEDIA_ROOT = "media/"

# Login/Logout Redirect URLs
LOGIN_REDIRECT_URL = "/jobs/search"
LOGOUT_REDIRECT_URL = "/account/login"

# TailWindCSS Settings
TAILWIND_APP_NAME = "tailwindcss"

INTERNAL_IPS = [
    "127.0.0.1",
]

# Compressor Settings
COMPRESS_ROOT = BASE_DIR / "tailwindcss/static"

COMPRESS_ENABLED = True

SITE_ID = 1

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

SOCIALACCOUNT_LOGIN_ON_GET=True

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_EMAIL_REQUIRED=True
# ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/accounts/register_info"
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_PREVENT_ENUMERATION = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_REDIRECT_URL ="/"
ACCOUNT_LOGOUT_ON_GET = False
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"


# # メールサーバーへの接続設定
# # Gmailのアドレス、Gmailのアプリ用パスワードは
# # お使いのものを入力してください
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587                     # SMPTサーバーのポート番号
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True # SMTP サーバと通信する際に TLS (セキュア) 接続を使う
EMAIL_BACKEND = 'accounts.backend.LoggingEmailBackend'


STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

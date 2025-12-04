from datetime import timedelta
from pathlib import Path
from typing import cast

import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY", default="dev-key-change-in-production")
DEBUG = config("DEBUG", default=False, cast=bool)
_allowed_hosts_str = cast(str, config("ALLOWED_HOSTS", default="", cast=str))
ALLOWED_HOSTS = [host.strip() for host in _allowed_hosts_str.split(",") if host.strip()]

# Security headers
# SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
# SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
# CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = "DENY"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Owned apps
    "registration_profile",
    "author",
    "cookbook",
    "ingredient",
    "recipe",
    "user",
    # Third party apps
    "rest_framework",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "recipe_cookbok_management.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "recipe_cookbok_management.wsgi.application"


# Database - Use PostgreSQL in production
_database_url = config("DATABASE_URL", default=None)
if _database_url:
    DATABASES = {"default": dj_database_url.config(default=cast(str, _database_url))}
else:
    # Development: SQLite3
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# user should be the name of your app, User should be the name of your model
AUTH_USER_MODEL = "user.User"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "recipe_cookbok_management.authentication.JWTAuthenticationWithoutBearer",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "recipe": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token (without 'Bearer' prefix)",
        }
    },
    "PERSIST_AUTH": True,
}

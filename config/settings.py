"""
Django settings for config project.
Production-ready: all secrets from .env, no fallbacks.
"""

import sys
from pathlib import Path
from decouple import config, Csv  # 👈 Читаем переменные строго из .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Добавляем папку apps в sys.path для импортов
sys.path.insert(0, str(BASE_DIR / "apps"))

# =============================================================================
# SECURITY & SECRETS (STRICT MODE - NO FALLBACKS)
# =============================================================================
# Если переменной нет в .env — приложение упадёт с понятной ошибкой.
# Это правильно: лучше узнать о проблеме сразу, чем работать с небезопасными дефолтами.

SECRET_KEY = config("SECRET_KEY")  # Обязательная переменная
DEBUG = config("DEBUG", cast=bool)  # Обязательная, приводим к bool
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())  # Список через запятую

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "django_filters",
    "rest_framework",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    # Local apps
    "claims",
    "core",
    "machines",
    "maintenance",
    "organizations",
    "references",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =============================================================================
# DATABASE (STRICT MODE)
# =============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "OPTIONS": {
            "connect_timeout": 5,
            "sslmode": "disable",
        },
    }
}

# =============================================================================
# AUTH & ALLAUTH
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

ACCOUNT_ADAPTER = "users.adapters.MyAccountAdapter"
ACCOUNT_ALLOW_SIGNUPS = False
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # <-- Исходники (наши правки)
STATIC_ROOT = BASE_DIR / "staticfiles"  # <-- Сборка для продакшена

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# DJANGO REST FRAMEWORK
# =============================================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# =============================================================================
# DRF-SPECTACULAR (Swagger)
# =============================================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "Силант API",
    "DESCRIPTION": "API для сервиса отслеживания состояния техники ЧЗСА",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "TAGS": [
        {"name": "machines", "description": "Каталог техники"},
        {"name": "maintenance", "description": "Журнал ТО"},
        {"name": "claims", "description": "Рекламации"},
        {"name": "references", "description": "Справочники"},
    ],
}

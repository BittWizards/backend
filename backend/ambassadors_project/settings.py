# flake8: noqa
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY", "83(vot%*rpken0wm#0lt!defrrf0%%=hl$ey8(b20%l8a07#f^"
)  # default key is just for django test

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split(" ")

DOMAIN = os.getenv("DOMAIN", "localhost:8000")

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "debug_toolbar",
    "django_filters",
    "drf_spectacular",
    # project apps
    "ambassadors",
    "users",
    "orders",
    "content",
    "bot",
    # "websocket",
    "mailing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    # Меняется конечная цифра в зависимости от старта контейнеров
    INTERNAL_IPS = [
        ip[: ip.rfind(".")] + f".{x}" for ip in ips for x in range(1, 5)
    ] + [
        "127.0.0.1",
    ]

    INSTALLED_APPS.insert(6, "corsheaders")
    MIDDLEWARE.insert(2, "corsheaders.middleware.CorsMiddleware")

    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = [f"https://{DOMAIN}", f"http://{DOMAIN}"]

SPECTACULAR_SETTINGS = {
    "TITLE": "Ambassadors Project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVERS": [{"url": f"https://{DOMAIN}"}, {"url": f"http://{DOMAIN}"}],
    "COMPONENT_SPLIT_REQUEST": True,
}

REST_FRAMEWORK = {
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    # ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ROOT_URLCONF = "ambassadors_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "ambassadors_project.wsgi.application"
ASGI_APPLICATION = "ambassadors_project.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django_dev"),
        "USER": os.getenv("POSTGRES_USER", "django_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "django_pass"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

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

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Using custom user model
AUTH_USER_MODEL = "users.User"

CELERY_BROKER_URL = os.environ.get("BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "RESULT_BACKEND", "redis://redis:6379/0"
)
CELERY_TIMEZONE = "Europe/Moscow"

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Email Settings
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER", "ambassadors@yandex.ru")
if os.getenv("USE_SMTP", "False").lower() == "true":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")

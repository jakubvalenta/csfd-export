from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "django-insecure-egkq%!g9k8k*3ux-ti22-+^#zlcq(sxslyi&z78r+lxz%93ww8"

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".local"]

INSTALLED_APPS = ["django.contrib.staticfiles", "csfd_export"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "csfd_export.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

TIME_ZONE = "UTC"

USE_I18N = False

STATIC_URL = "static/"
STATIC_ROOT = str(BASE_DIR.parent / "public")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler"}},
    "loggers": {"csfd_export": {"level": "INFO", "handlers": ["console"]}},
}

SCRAPER_INTERVAL = 1
SCRAPER_TIMEOUT = 10
SCRAPER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; rv:131.0) Gecko/20100101 Firefox/131.0"
)

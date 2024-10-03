import os
from pathlib import Path

from csfd_export.settings import *  # noqa: F401, F403

ALLOWED_HOSTS = [os.environ["ALLOWED_HOST"]]
DEBUG = False
SECRET_KEY = (
    Path(os.environ.get("SECRET_KEY_FILE", "/run/keys/csfd-export-secret-key"))
    .read_text()
    .strip()
)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "csfd-export",
        "USER": "robot",
        "CONN_MAX_AGE": 300,
    }
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

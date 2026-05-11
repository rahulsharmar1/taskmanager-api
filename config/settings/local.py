from .base import * # noqa: F401, F403
from decouple import config

DEBUG = config("DEBUG", default=True, cast=bool)

# SQLite — file-based, zero config, perfect for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Make DRF's browsable API available locally for easy exploration
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

# Main settings
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = ["127.0.0.1"]

INTERNAL_IPS = ["127.0.0.1"]

# Application definition
include(
    "components/applications.py",
)

# Database
include(
    "components/database.py",
)


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


# Internationalization
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATH = ["domains/locale"]


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

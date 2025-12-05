from .base import *

DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

# local Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    },
    "OPTIONS": {
        "sslmode": os.getenv("DB_SSL_MODE", "require"),
    },
}


# {
#   "email": "diallokesso923@gmail.com",
#   "username": "kesso",
#   "password": "diallokesso923@"
# }
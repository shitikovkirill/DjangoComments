from .base import *  # noqa: F403 F401
import os

DEBUG = os.environ.get("DEBUG_MODE", "NO") == "YES"

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOST", "")]

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.environ.get("MAILGUN_ACCESS_KEY")
MAILGUN_SERVER_NAME = os.environ.get("MAILGUN_SERVER_NAME")

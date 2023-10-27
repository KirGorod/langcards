import os
from .base import *

DEBUG = False

# Other development-specific settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['langcards.fun', 'www.langcards.fun', 'blenemy.github.io', '64.226.100.40']
CSRF_TRUSTED_ORIGINS = ['https://langcards.fun', 'https://www.langcards.fun']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_ALLOWED_ORIGINS = ["https://blenemy.github.io", "http://localhost:3000"]
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

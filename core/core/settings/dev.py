import os
from .base import *

DEBUG = True
SQL_LOGGING = True

# Other development-specific settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['*']

if SQL_LOGGING:
    MIDDLEWARE = MIDDLEWARE + ['core.middleware.SQLMiddleware']
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }

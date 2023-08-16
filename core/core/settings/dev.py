import os
from .base import *

DEBUG = True

# Other development-specific settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['*']

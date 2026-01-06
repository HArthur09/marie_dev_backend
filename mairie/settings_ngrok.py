# backend/votre_projet/settings_ngrok.py
from .settings import *

# Désactiver le debug en production
DEBUG = False

# Configuration de sécurité pour ngrok
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Allowed hosts dynamique
import os
NGROK_URL = os.environ.get('NGROK_URL', '')
if NGROK_URL:
    ALLOWED_HOSTS = [
        NGROK_URL.replace('https://', '').replace('http://', '').split(':')[0],
        'localhost',
        '127.0.0.1',
    ]

# Logging pour ngrok
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
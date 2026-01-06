"""
ASGI config for mairie project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

settings_module = 'mairie.mairie.deployement_settings' if 'Render_external_hostname' in os.environ else 'mairie.mairie.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_asgi_application()

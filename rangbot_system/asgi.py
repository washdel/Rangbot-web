"""
ASGI config for rangbot_system project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rangbot_system.settings')

application = get_asgi_application()


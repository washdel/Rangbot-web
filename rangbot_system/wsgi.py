"""
WSGI config for rangbot_system project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rangbot_system.settings')

application = get_wsgi_application()


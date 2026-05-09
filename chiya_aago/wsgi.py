"""
WSGI config for chiya_aago project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chiya_aago.settings")

application = get_wsgi_application()

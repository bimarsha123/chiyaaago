"""
ASGI config for chiya_aago project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chiya_aago.settings")

application = get_asgi_application()

"""
ASGI config for bucket_list project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bucket_list.settings')

application = get_asgi_application()
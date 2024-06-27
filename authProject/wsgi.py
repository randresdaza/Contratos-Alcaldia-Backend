"""
WSGI config for authProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authProject.settings')

BASE_DIR = Path(__file__).resolve().parent.parent

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'static'))

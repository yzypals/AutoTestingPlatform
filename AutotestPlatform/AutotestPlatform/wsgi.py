"""
WSGI config for AutotestPlatform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys
sys.path.append('E:/mygit/AutotestPlatform/')
sys.path.append('E:/mygit/AutotestPlatform/AutotestPlatform')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutotestPlatform.settings")

application = get_wsgi_application()

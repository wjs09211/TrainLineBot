"""
WSGI config for TrainLineBot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from TrainLineBot import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrainLineBot.settings')

if settings.IS_HEROKU:
    from dj_static import Cling
    application = Cling(get_wsgi_application())
else:
    application = get_wsgi_application()

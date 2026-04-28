"""
WSGI config for the Sky Engineering Portal.

Django uses this file as the entry point when the project is served by a WSGI
server.  For coursework, runserver still uses this standard configuration.
"""

import os
from django.core.wsgi import get_wsgi_application

# Connect this WSGI file to the project's settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sky_engineering.settings')

# application is the callable used by web servers to run the Django project.
application = get_wsgi_application()

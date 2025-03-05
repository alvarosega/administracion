"""
WSGI config for admin_negocios project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_negocios.settings")

application = get_wsgi_application()


from django.shortcuts import render

def index(request):
    """Vista principal que muestra el panel según el rol del usuario."""
    es_admin = request.user.rol == 'admin'
    return render(request, 'index.html', {'es_admin': es_admin})
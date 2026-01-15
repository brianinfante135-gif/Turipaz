import os
from django.core.wsgi import get_wsgi_application

# Esto ya lo tienes correcto según tu carpeta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

application = get_wsgi_application()

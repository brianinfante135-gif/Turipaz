from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contacto.urls')), # Esto es lo que activa todo lo anterior
]

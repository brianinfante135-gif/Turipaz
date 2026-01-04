from django.contrib import admin
from django.urls import path
from contacto import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('interfaz/', views.interfaz, name='interfaz'),
    path('registro/', views.registro, name='registro'),
    path('recuperar_password/', views.recuperar_password, name='recuperar_password'),
    path('reservacion/', views.reservacion, name='reservacion'),
    path('tur1/', views.tur1, name='tur1'),
    path('tur2/', views.tur2, name='tur2'),
    path('tur3/', views.tur3, name='tur3'),
    path('tur4/', views.tur4, name='tur4'),
    path('tur5/', views.tur5, name='tur5'),
    path('tur6/', views.tur6, name='tur6'),
    
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

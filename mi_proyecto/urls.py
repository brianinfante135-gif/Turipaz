from django.contrib import admin
from django.urls import path
from mi_proyecto import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),  # Página principal (login)
    path('interfaz/', views.interfaz, name='interfaz'),
    path('tur1/', views.tur1, name='tur1'),
     path('registro/', views.registro, name='registro'),
    path('tur2/', views.tur2, name='tur2'),
    path('tur3/', views.tur3, name='tur3'),
    path('tur4/', views.tur4, name='tur4'),
    path('tur5/', views.tur5, name='tur5'),
    path('tur6/', views.tur6, name='tur6'),
    path('reservacion/', views.reservacion, name='reservacion'),
    path('recuperar_password/', views.recuperar_password, name='recuperar_password'),
    
]

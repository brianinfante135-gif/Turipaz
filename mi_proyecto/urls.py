from django.urls import path
from . import views # El punto (.) es clave aquí

urlpatterns = [
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
    path('index/', views.index, name='index'), # Tu CRUD
]



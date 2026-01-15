from django.contrib import admin
from .models import Reservacion, DestinoTuristico, Usuario, Estadistica

@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_completo', 'destino', 'fecha_visita', 'numero_personas', 'estado', 'activo']
    list_filter = ['estado', 'destino', 'fecha_visita', 'activo']
    search_fields = ['nombre_completo', 'email', 'telefono']
    date_hierarchy = 'fecha_visita'
    ordering = ['-fecha_creacion']
    list_per_page = 20

@admin.register(DestinoTuristico)
class DestinoTuristicoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'capacidad_maxima', 'precio_entrada', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nombre', 'apellido', 'correo', 'edad', 'fecha_registro']
    search_fields = ['username', 'nombre', 'apellido', 'correo']
    ordering = ['-fecha_registro']
    list_per_page = 20

@admin.register(Estadistica)
class EstadisticaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'total_reservaciones', 'total_visitantes', 'destino_mas_popular']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'


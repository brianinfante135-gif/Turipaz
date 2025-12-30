from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone


class Reservacion(models.Model):
    """
    Modelo para gestionar las reservaciones turísticas de TURIPAZ
    Los Reyes La Paz
    """
    
    # Opciones de destinos turísticos
    DESTINOS = [
        ('zona_arqueologica', 'Zona Arqueológica'),
        ('parque_soraya', 'Parque Soraya Jiménez'),
        ('santa_marta', 'Santa Marta'),
        ('parroquia_divino', 'Parroquia Divino Salvador'),
        ('volcan_caldera', 'Volcán de la Caldera'),
        ('parque_ciencia', 'Parque de la Ciencia'),
    ]
    
    # Estados de la reservación
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    # Validador de teléfono (10 dígitos)
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="El teléfono debe tener exactamente 10 dígitos"
    )
    
    # Campos del modelo
    nombre_completo = models.CharField(
        max_length=200,
        verbose_name="Nombre Completo",
        help_text="Nombre completo del cliente"
    )
    
    email = models.EmailField(
        verbose_name="Correo Electrónico",
        help_text="Dirección de correo electrónico del cliente"
    )
    
    telefono = models.CharField(
        max_length=10,
        validators=[phone_validator],
        verbose_name="Teléfono",
        help_text="Número telefónico de 10 dígitos"
    )
    
    destino = models.CharField(
        max_length=50,
        choices=DESTINOS,
        verbose_name="Destino Turístico",
        help_text="Lugar a visitar"
    )
    
    fecha_visita = models.DateField(
        verbose_name="Fecha de Visita",
        help_text="Fecha programada para la visita"
    )
    
    numero_personas = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="Número de Personas",
        help_text="Cantidad de personas (1-50)"
    )
    
    comentarios = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comentarios",
        help_text="Información adicional o solicitudes especiales"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        verbose_name="Estado de Reservación"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la reservación está activa"
    )
    
    class Meta:
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['fecha_visita', 'destino']),
            models.Index(fields=['email']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"Reserva #{self.pk} - {self.nombre_completo} - {self.get_destino_display()}"
    
    def clean(self):
        """Validación personalizada"""
        from django.core.exceptions import ValidationError
        
        # Validar que la fecha de visita no sea en el pasado
        if self.fecha_visita and self.fecha_visita < timezone.now().date():
            raise ValidationError({
                'fecha_visita': 'La fecha de visita no puede ser en el pasado'
            })
    
    def save(self, *args, **kwargs):
        """Override del método save para validaciones adicionales"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def dias_restantes(self):
        """Calcula los días restantes hasta la fecha de visita"""
        if self.fecha_visita:
            delta = self.fecha_visita - timezone.now().date()
            return delta.days
        return None
    
    @property
    def es_hoy(self):
        """Verifica si la visita es hoy"""
        return self.fecha_visita == timezone.now().date()
    
    @property
    def es_proxima(self):
        """Verifica si la visita es dentro de los próximos 7 días"""
        dias = self.dias_restantes
        return dias is not None and 0 <= dias <= 7


class Estadistica(models.Model):
    """
    Modelo para almacenar estadísticas agregadas del sistema
    """
    fecha = models.DateField(
        unique=True,
        verbose_name="Fecha"
    )
    
    total_reservaciones = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Reservaciones"
    )
    
    total_visitantes = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Visitantes"
    )
    
    destino_mas_popular = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Destino Más Popular"
    )
    
    class Meta:
        verbose_name = "Estadística"
        verbose_name_plural = "Estadísticas"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Estadísticas del {self.fecha}"


class DestinoTuristico(models.Model):
    """
    Modelo para información detallada de cada destino turístico
    """
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Nombre del Destino"
    )
    
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del destino"
    )
    
    capacidad_maxima = models.PositiveIntegerField(
        default=50,
        verbose_name="Capacidad Máxima",
        help_text="Número máximo de visitantes por día"
    )
    
    precio_entrada = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name="Precio de Entrada"
    )
    
    horario_apertura = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Horario de Apertura"
    )
    
    horario_cierre = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Horario de Cierre"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Destino Activo"
    )
    
    imagen = models.ImageField(
        upload_to='destinos/',
        null=True,
        blank=True,
        verbose_name="Imagen del Destino"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    class Meta:
        verbose_name = "Destino Turístico"
        verbose_name_plural = "Destinos Turísticos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def reservaciones_del_dia(self, fecha=None):
        """Retorna el número de reservaciones para una fecha específica"""
        if fecha is None:
            fecha = timezone.now().date()
        return Reservacion.objects.filter(
            destino=self.nombre,
            fecha_visita=fecha,
            activo=True
        ).count()
    
    def capacidad_disponible(self, fecha=None):
        """Calcula la capacidad disponible para una fecha"""
        reservadas = self.reservaciones_del_dia(fecha)
        return max(0, self.capacidad_maxima - reservadas)
    
    from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    edad = models.IntegerField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"

from django import forms
from .models import Reservacion, DestinoTuristico, Usuario

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['nombre_completo', 'email', 'telefono', 'destino', 'fecha_visita', 
                  'numero_personas', 'comentarios', 'estado']
        widgets = {
            'fecha_visita': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }

class DestinoTuristicoForm(forms.ModelForm):
    class Meta:
        model = DestinoTuristico
        fields = ['nombre', 'descripcion', 'capacidad_maxima', 'precio_entrada',
                  'horario_apertura', 'horario_cierre', 'activo', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'horario_apertura': forms.TimeInput(attrs={'type': 'time'}),
            'horario_cierre': forms.TimeInput(attrs={'type': 'time'}),
        }

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'edad', 'username', 'password']

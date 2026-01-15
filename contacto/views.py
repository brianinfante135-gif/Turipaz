from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import hashlib
import secrets
import json

# Importa tus modelos y formularios DESDE TU APP (asumiendo que se llama 'contacto')
from .models import Reservacion, DestinoTuristico, Usuario, Reserva 
from .forms import ReservacionForm, DestinoTuristicoForm, UsuarioForm

# --- VISTAS PRINCIPALES ---

def inicio(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                usuario = Usuario.objects.get(username=username, password=password_hash)
                request.session['user_id'] = str(usuario.id)
                request.session['username'] = usuario.username
                request.session['nombre_completo'] = f"{usuario.nombre} {usuario.apellido}"
                return redirect('interfaz')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'inicio.html')

def registro(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('correo')
            edad = request.POST.get('edad')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not all([nombre, apellido, correo, edad, username, password]):
                messages.error(request, 'Todos los campos son obligatorios')
                return render(request, 'registro.html')
            
            if Usuario.objects.filter(username=username).exists() or Usuario.objects.filter(correo=correo).exists():
                messages.error(request, 'El usuario o correo ya existen')
                return render(request, 'registro.html')
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            nuevo_usuario = Usuario.objects.create(
                nombre=nombre, apellido=apellido, correo=correo,
                edad=int(edad), username=username, password=password_hash
            )
            
            request.session['user_id'] = str(nuevo_usuario.id)
            request.session['username'] = nuevo_usuario.username
            request.session['nombre_completo'] = f"{nuevo_usuario.nombre} {nuevo_usuario.apellido}"
            return redirect('interfaz')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
    return render(request, 'registro.html')

def recuperar_password(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            usuario = Usuario.objects.get(correo=correo)
            nueva_password = secrets.token_urlsafe(8)
            password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()

            usuario.password = password_hash
            usuario.save()

            messages.success(request, f'Contraseña restablecida para {correo}.')
            messages.info(request, f'TU NUEVA CONTRASEÑA ES: {nueva_password}')
            return redirect('inicio')

        except Usuario.DoesNotExist:
            messages.error(request, 'El correo no está registrado.')
        except Exception as e:
            print(f"Error crítico: {e}")
            messages.error(request, 'Hubo un error interno.')
            
    return render(request, 'recuperar_password.html')

def interfaz(request):
    # 1. Verificar si el usuario está logueado
    if 'user_id' not in request.session:
        return redirect('inicio')

    # 2. Si el usuario envía el formulario de reserva
    if request.method == 'POST':
        try:
            # Creamos la reserva usando el modelo 'Reserva' (o 'Reservacion' según tu models.py)
            Reserva.objects.create(
                nombre=request.POST.get('name'),
                email=request.POST.get('email'),
                telefono=request.POST.get('phone'),
                destino=request.POST.get('destination'),
                fecha=request.POST.get('date'),
                personas=request.POST.get('people'),
                mensaje=request.POST.get('message')
            )
            messages.success(request, '¡Tu reserva ha sido enviada con éxito!')
            return redirect('interfaz')
        except Exception as e:
            messages.error(request, f'Error al guardar la reserva: {str(e)}')

    return render(request, 'interfaz.html')

# Vistas de turismo
def tur1(request): 
    return render(request, 'tur1.html')

def tur2(request): 
    return render(request, 'tur2.html')

def tur3(request): 
    return render(request, 'tur3.html')

def tur4(request): 
    return render(request, 'tur4.html')

def tur5(request): 
    return render(request, 'tur5.html')

def tur6(request): 
    return render(request, 'tur6.html')

# contacto/views.py

def reservacion(request):
    # Si solo quieres que cargue la página por ahora:
    return render(request, 'reservacion.html')

def index(request):
    # Obtener todos los datos
    reservaciones = Reservacion.objects.filter(activo=True).order_by('-fecha_creacion')
    destinos = DestinoTuristico.objects.filter(activo=True)
    usuarios = Usuario.objects.all()
    
    # Manejar formularios
    if request.method == 'POST':
        accion = request.POST.get('accion')
        tipo = request.POST.get('tipo')
        
        # RESERVACIONES
        if tipo == 'reservacion':
            if accion == 'crear':
                form = ReservacionForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Reservación creada exitosamente')
                    return redirect('index')
            elif accion == 'editar':
                pk = request.POST.get('id')
                reservacion = get_object_or_404(Reservacion, pk=pk)
                form = ReservacionForm(request.POST, instance=reservacion)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Reservación actualizada')
                    return redirect('index')
            elif accion == 'eliminar':
                pk = request.POST.get('id')
                reservacion = get_object_or_404(Reservacion, pk=pk)
                reservacion.activo = False
                reservacion.save()
                messages.success(request, 'Reservación eliminada')
                return redirect('index')
        
        # DESTINOS
        elif tipo == 'destino':
            if accion == 'crear':
                form = DestinoTuristicoForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Destino creado exitosamente')
                    return redirect('index')
            elif accion == 'editar':
                pk = request.POST.get('id')
                destino = get_object_or_404(DestinoTuristico, pk=pk)
                form = DestinoTuristicoForm(request.POST, request.FILES, instance=destino)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Destino actualizado')
                    return redirect('index')
            elif accion == 'eliminar':
                pk = request.POST.get('id')
                destino = get_object_or_404(DestinoTuristico, pk=pk)
                destino.activo = False
                destino.save()
                messages.success(request, 'Destino eliminado')
                return redirect('index')
        
        # USUARIOS
        elif tipo == 'usuario':
            if accion == 'crear':
                form = UsuarioForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Usuario creado exitosamente')
                    return redirect('index')
            elif accion == 'editar':
                pk = request.POST.get('id')
                usuario = get_object_or_404(Usuario, pk=pk)
                form = UsuarioForm(request.POST, instance=usuario)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Usuario actualizado')
                    return redirect('index')
            elif accion == 'eliminar':
                pk = request.POST.get('id')
                usuario = get_object_or_404(Usuario, pk=pk)
                usuario.delete()
                messages.success(request, 'Usuario eliminado')
                return redirect('index')
    
    context = {
        'reservaciones': reservaciones,
        'destinos': destinos,
        'usuarios': usuarios,
        'form_reservacion': ReservacionForm(),
        'form_destino': DestinoTuristicoForm(),
        'form_usuario': UsuarioForm(),
    }
    
    return render(request, 'index.html', context)


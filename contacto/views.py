from django.shortcuts import render, redirect
from django.contrib import messages
from contacto.models import Usuario
import hashlib
import secrets

# --- VISTAS ---

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

            # Mensajes que se mostrarán en la página de inicio al redirigir
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
    if 'user_id' not in request.session: return redirect('inicio')
    return render(request, 'interfaz.html')

def tur1(request): return render(request, 'tur1.html')
def tur2(request): return render(request, 'tur2.html')
def tur3(request): return render(request, 'tur3.html')
def tur4(request): return render(request, 'tur4.html')
def tur5(request): return render(request, 'tur5.html')
def tur6(request): return render(request, 'tur6.html')
def reservacion(request): return render(request, 'reservacion.html')
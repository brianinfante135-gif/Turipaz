from django.shortcuts import render, redirect
from django.contrib import messages
from contacto.models import Usuario
import hashlib
from django.core.mail import send_mail
from django.conf import settings
import secrets
import threading

# --- FUNCIÓN PARA ENVÍO EN SEGUNDO PLANO ---
def enviar_correo_async(asunto, mensaje, remitente, destinatario):
    try:
        send_mail(asunto, mensaje, remitente, [destinatario], fail_silently=False)
    except Exception as e:
        print(f"Error en envío de fondo: {e}")

# --- VISTAS ---

def inicio(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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

            # 1. GUARDADO PRIORITARIO
            usuario.password = password_hash
            usuario.save()

            asunto = 'Recuperación de contraseña - Turipaz'
            mensaje = f"Hola {usuario.nombre}, tu contraseña temporal es: {nueva_password}"
            
            # 2. LANZAR HILO (Thread) PARA ENVÍO INSTANTÁNEO
            hilo = threading.Thread(
                target=enviar_correo_async,
                args=(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, correo)
            )
            hilo.start()

            # 3. REDIRIGIR DE INMEDIATO (Evita el Error 502)
            messages.success(request, f'Se está procesando el envío a {correo}.')
            return redirect('inicio')

        except Usuario.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
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
from django.shortcuts import render, redirect
from django.contrib import messages
from contacto.models import Usuario
import hashlib
from django.core.mail import send_mail
from django.conf import settings
import secrets

# Vista para inicio.html (LOGIN)
def inicio(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Encriptar la contraseña
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            usuario = Usuario.objects.get(username=username, password=password_hash)
            # Guardar en sesión
            request.session['user_id'] = str(usuario.id)
            request.session['username'] = usuario.username
            request.session['nombre_completo'] = f"{usuario.nombre} {usuario.apellido}"
            return redirect('interfaz')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'inicio.html')

# Vista para registro.html (REGISTRO)
def registro(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('correo')
            edad = request.POST.get('edad')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Validar que ningún campo esté vacío
            if not all([nombre, apellido, correo, edad, username, password]):
                messages.error(request, 'Todos los campos son obligatorios')
                return render(request, 'registro.html')
            
            # Verificar si el usuario ya existe
            if Usuario.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe')
                return render(request, 'registro.html')
            
            if Usuario.objects.filter(correo=correo).exists():
                messages.error(request, 'El correo ya está registrado')
                return render(request, 'registro.html')
            
            # Encriptar la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Crear el usuario
            nuevo_usuario = Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                edad=int(edad),
                username=username,
                password=password_hash
            )
            
            # INICIAR SESIÓN AUTOMÁTICAMENTE
            request.session['user_id'] = str(nuevo_usuario.id)
            request.session['username'] = nuevo_usuario.username
            request.session['nombre_completo'] = f"{nuevo_usuario.nombre} {nuevo_usuario.apellido}"
            
            messages.success(request, f'¡Bienvenido {nombre}!')
            return redirect('interfaz')
            
        except ValueError as ve:
            print(f"Error de validación: {str(ve)}")
            messages.error(request, 'Error en los datos ingresados')
            return render(request, 'registro.html')
            
        except Exception as e:
            print(f"ERROR COMPLETO: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al registrar usuario: {str(e)}')
            return render(request, 'registro.html')
    
    return render(request, 'registro.html')

# Vista para recuperar contraseña
# ... (tus otros imports)

def recuperar_password(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            # Buscamos al usuario por correo
            usuario = Usuario.objects.get(correo=correo)
            
            # 1. Generamos la nueva contraseña temporal
            nueva_password = secrets.token_urlsafe(8)
            password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()

            # 2. GUARDADO PRIORITARIO: Cambiamos la clave en la BD de inmediato
            # Esto asegura que el usuario pueda entrar aunque el correo tarde
            usuario.password = password_hash
            usuario.save()

            # 3. Preparamos el mensaje
            asunto = 'Recuperación de contraseña - Turipaz'
            mensaje = f"Hola {usuario.nombre}, tu contraseña temporal es: {nueva_password}"
            
            try:
                # 4. Intentamos enviar el correo
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [correo],
                    fail_silently=False,
                )
                messages.success(request, f'Se ha enviado un correo a {correo}')
            except Exception as e:
                # Si Gmail falla o tarda mucho, el usuario ya tiene su clave cambiada
                print(f"Error en envío de correo (pero clave guardada): {e}")
                messages.warning(request, 'La clave se cambió, pero hubo un retraso con el correo. Intenta revisar en unos minutos.')
            
            # 5. Redirigimos rápido al inicio para evitar el Error 502 de Render
            return redirect('inicio')

        except Usuario.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    return render(request, 'recuperar_password.html')
# Vista para interfaz
def interfaz(request):
    # Verificar si el usuario está logueado
    if 'user_id' not in request.session:
        return redirect('inicio')
    return render(request, 'interfaz.html')

# Resto de vistas
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

def reservacion(request):
    return render(request, 'reservacion.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from contacto.models import Usuario, Reservacion
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
            return redirect('interfaz')  # Cambiado a 'index' para que vaya a la página principal
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
            return redirect('index')
            
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
def recuperar_password(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        
        try:
            usuario = Usuario.objects.using('default').get(correo=correo)
            
            # Generar nueva contraseña temporal
            nueva_password = secrets.token_urlsafe(8)
            
            # Encriptar la nueva contraseña
            password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()
            
            # Actualizar la contraseña en la base de datos
            usuario.password = password_hash
            usuario.save(using='default')
            
            # Enviar correo con la nueva contraseña
            asunto = 'Recuperación de contraseña - Turipaz'
            mensaje = f"""
Hola {usuario.nombre} {usuario.apellido},

Has solicitado recuperar tu contraseña de Turipaz.

Tu nueva contraseña temporal es: {nueva_password}

Usuario: {usuario.username}
Contraseña temporal: {nueva_password}

Por favor, inicia sesión con esta contraseña y cámbiala por una nueva.

Saludos,
Equipo Turipaz
            """
            
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [correo],
                fail_silently=False,
            )
            
            messages.success(request, f'Se ha enviado un correo a {correo} con tu nueva contraseña')
            
        except Usuario.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {str(e)}')
    
    return render(request, 'recuperar_password.html')

# Vista para interfaz.html (Dashboard/Panel de usuario)
def interfaz(request):
    if 'user_id' not in request.session:
        return redirect('inicio')  # Redirigir al login si no hay sesión
    
    return render(request, 'interfaz.html')

# Vista principal INDEX.HTML - Página de turismo con formulario de reserva
def index(request):
    if request.method == 'POST':
        try:
            # Capturar datos del formulario
            nombre = request.POST.get('name')
            email = request.POST.get('email')
            telefono = request.POST.get('phone')
            destino = request.POST.get('destination')
            fecha = request.POST.get('date')
            personas = request.POST.get('people')
            mensaje = request.POST.get('message', '')
            
            # Validar que los campos obligatorios no estén vacíos
            if not all([nombre, email, telefono, destino, fecha, personas]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Todos los campos obligatorios deben estar llenos'
                }, status=400)
            
            # Crear la reservación en la base de datos
            reserva = Reservacion.objects.create(
                nombre_completo=nombre,
                email=email,
                telefono=telefono,
                destino=destino,
                fecha_visita=fecha,
                numero_personas=int(personas),
                comentarios=mensaje
            )
            
            print(f"✅ Reserva guardada exitosamente - ID: {reserva.id}")
            print(f"   Nombre: {nombre}")
            print(f"   Destino: {destino}")
            print(f"   Fecha: {fecha}")
            
            # Respuesta exitosa en formato JSON
            return JsonResponse({
                'status': 'success',
                'message': 'Reserva guardada correctamente'
            })
            
        except ValueError as ve:
            print(f"❌ Error de valor: {ve}")
            return JsonResponse({
                'status': 'error',
                'message': 'Error en el formato de los datos'
            }, status=400)
            
        except Exception as e:
            print(f"❌ Error al guardar reserva: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'message': f'Error al procesar la reserva: {str(e)}'
            }, status=500)
    
    # Si es GET, mostrar la página principal
    return render(request, 'interfaz.html')

# Resto de vistas de destinos turísticos
def tur1(request):
    return render(request, 'interfaz/tur1.html')

def tur2(request):
    return render(request, 'interfaz/tur2.html')

def tur3(request):
    return render(request, 'interfaz/tur3.html')

def tur4(request):
    return render(request, 'interfaz/tur4.html')

def tur5(request):
    return render(request, 'interfaz/tur5.html')

def tur6(request):
    return render(request, 'interfaz/tur6.html')

# Vista para ver todas las reservaciones (opcional - para admin)
def reservacion(request):
    if 'user_id' not in request.session:
        return redirect('inicio')
    
    reservas = Reservacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'reservacion.html', {'reservas': reservas})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from contacto.models import Usuario, Reservacion, DestinoTuristico
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
            return redirect('inicio')
            
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
            # 1. Identificar acción (para el CRUD del panel)
            accion = request.POST.get('accion')
            tipo = request.POST.get('tipo')

            # Lógica para ELIMINAR
            if accion == 'eliminar':
                id_item = request.POST.get('id')
                Reservacion.objects.filter(id=id_item).delete()
                return redirect('index')

            # 2. Captura de datos (mapeo doble para interfaz.html e index.html)
            nombre = request.POST.get('name') or request.POST.get('nombre_completo')
            email = request.POST.get('email')
            telefono = request.POST.get('phone') or request.POST.get('telefono')
            destino = request.POST.get('destination') or request.POST.get('destino')
            fecha = request.POST.get('date') or request.POST.get('fecha_visita')
            personas = request.POST.get('people') or request.POST.get('numero_personas')
            mensaje = request.POST.get('message', '') or request.POST.get('comentarios', '')
            
            # 3. Validación básica
            if not all([nombre, email, telefono, destino, fecha, personas]):
                return JsonResponse({'status': 'error', 'message': 'Faltan campos obligatorios'}, status=400)

            # 4. Guardar en la base de datos
            # Nota: Usamos los valores que ya validaste en el HTML (ej: 'volcan_caldera')
            reserva = Reservacion.objects.create(
                nombre_completo=nombre,
                email=email,
                telefono=telefono,
                destino=destino,
                fecha_visita=fecha,
                numero_personas=int(personas),
                comentarios=mensaje,
                estado=request.POST.get('estado', 'pendiente')
            )
            
            print(f"✅ Reserva guardada con éxito. ID: {reserva.id}")

            # 5. Respuesta según el origen
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Reserva guardada correctamente'})
            
            return redirect('index')

        except Exception as e:
            print(f"❌ Error en POST index: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # --- LÓGICA PARA MOSTRAR LA TABLA (GET) ---
    # Esto es lo que hace que tu tabla deje de estar vacía
    todas_las_reservas = Reservacion.objects.all().order_by('-fecha_creacion')
    todos_los_destinos = DestinoTuristico.objects.all()

    contexto = {
        'reservaciones': todas_las_reservas, # Debe ser 'reservaciones' para tu HTML
        'destinos': todos_los_destinos,
    }
    
    return render(request, 'index.html', contexto)

# Resto de vistas de destinos turísticos
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

# Vista para ver todas las reservaciones (opcional - para admin)
def reservacion(request):
    if 'user_id' not in request.session:
        return redirect('inicio')
    
    reservas = Reservacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'reservacion.html', {'reservas': reservas})








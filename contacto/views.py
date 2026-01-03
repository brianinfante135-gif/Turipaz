from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from contacto.models import Usuario
import hashlib
import secrets
import json
from datetime import datetime

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
    if 'user_id' not in request.session: 
        return redirect('inicio')
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

# Vista de reservaciones (renderiza el HTML)
def reservacion(request): 
    return render(request, 'reservacion.html')


# --- API PARA RESERVACIONES ---

# API - Listar todas las reservaciones
@require_http_methods(["GET"])
def listar_reservaciones(request):
    try:
        # Aquí deberías obtener las reservaciones de tu base de datos
        # Ejemplo: reservations = Reservacion.objects.all().values()
        # Por ahora devuelvo un ejemplo vacío
        reservations = []
        
        return JsonResponse({
            'success': True,
            'reservations': list(reservations)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# API - Crear nueva reservación
@csrf_exempt
@require_http_methods(["POST"])
def crear_reservacion(request):
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        required_fields = ['name', 'email', 'phone', 'destination', 'date', 'people']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'message': f'Campo requerido: {field}'
                }, status=400)
        
        # Aquí deberías crear la reservación en tu base de datos
        # Ejemplo:
        # from .models import Reservacion
        # reservacion = Reservacion.objects.create(
        #     name=data['name'],
        #     email=data['email'],
        #     phone=data['phone'],
        #     destination=data['destination'],
        #     date=data['date'],
        #     people=data['people'],
        #     comments=data.get('comments', '')
        # )
        
        print(f"✅ Nueva reservación: {data['name']} - {data['destination']} - {data['date']}")
        
        return JsonResponse({
            'success': True,
            'message': 'Reservación creada exitosamente'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        print(f"❌ Error al crear reservación: {e}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# API - Eliminar reservación
@csrf_exempt
@require_http_methods(["POST"])
def eliminar_reservacion(request, id):
    try:
        # Aquí deberías eliminar de tu base de datos
        # Ejemplo:
        # from .models import Reservacion
        # reservacion = Reservacion.objects.get(id=id)
        # reservacion.delete()
        
        print(f"🗑️ Reservación eliminada: {id}")
        
        return JsonResponse({
            'success': True,
            'message': 'Reservación eliminada'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# API - Obtener estadísticas
@require_http_methods(["GET"])
def estadisticas(request):
    try:
        # Aquí deberías calcular desde tu base de datos
        # Ejemplo:
        # from .models import Reservacion
        # from django.db.models import Sum
        # today = datetime.now().date()
        # 
        # total = Reservacion.objects.count()
        # total_people = Reservacion.objects.aggregate(Sum('people'))['people__sum'] or 0
        # today_count = Reservacion.objects.filter(date=today).count()
        
        stats = {
            'totalReservations': 0,
            'totalPeople': 0,
            'todayReservations': 0
        }
        
        return JsonResponse({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
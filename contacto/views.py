from django.shortcuts import render

# Cambia 'contacto' por 'inicio'
def inicio(request): 
    return render(request, 'inicio.html')
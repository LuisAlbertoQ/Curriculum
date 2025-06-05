from django.shortcuts import render, get_object_or_404
from .models import Proyecto, DatosPersonales

def home(request):
    proyectos = Proyecto.objects.all()
    datos_personales = DatosPersonales.objects.first()
    return render(request, 'curriculum/home.html', {
        'proyectos': proyectos,
        'datos_personales': datos_personales
    })

def proyecto_detalle(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    return render(request, 'curriculum/proyecto_detalle.html', {
        'proyecto': proyecto
    })

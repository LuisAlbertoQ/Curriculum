# curriculum/admin.py

from django.contrib import admin
from .models import Proyecto, ImagenProyecto, DatosPersonales

class ImagenProyectoInline(admin.TabularInline):
    model = ImagenProyecto
    extra = 1  # Número de formularios vacíos que muestra por defecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link_github')
    search_fields = ('titulo',)
    inlines = [ImagenProyectoInline]
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'link_github')
        }),
        ('Tecnologías', {
            'fields': ('tecnologias', 'frontend', 'backend', 'base_datos', 'otras_librerias')
        }),
    )


@admin.register(ImagenProyecto)
class ImagenProyectoAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'imagen')

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')

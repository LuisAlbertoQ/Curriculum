from django.contrib import admin
from django.utils.html import format_html
from .models import DatosPersonales, Proyecto, ImagenProyecto

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'ubicacion', 'updated_at']
    search_fields = ['nombre', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email', 'telefono', 'ubicacion')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Redes Sociales', {
            'fields': ('linkedin', 'github'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ImagenProyectoInline(admin.TabularInline):
    model = ImagenProyecto
    extra = 1
    fields = ['imagen', 'titulo', 'descripcion', 'orden']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('orden')

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 
        'estado', 
        'destacado', 
        'fecha_inicio', 
        'fecha_fin', 
        'imagen_count',
        'updated_at'
    ]
    list_filter = ['estado', 'destacado', 'fecha_inicio', 'created_at']
    search_fields = ['titulo', 'descripcion', 'tecnologias']
    list_editable = ['destacado', 'estado']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ImagenProyectoInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('titulo', 'descripcion', 'descripcion_corta', 'estado', 'destacado', 'orden')
        }),
        ('Enlaces', {
            'fields': ('link_github', 'link_demo'),
            'classes': ('collapse',)
        }),
        ('Stack Tecnológico', {
            'fields': ('tecnologias', 'frontend', 'backend', 'base_datos', 'otras_librerias'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def imagen_count(self, obj):
        count = obj.imagenes.count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{} imagen{}</span>',
                count,
                's' if count != 1 else ''
            )
        return format_html('<span style="color: red;">Sin imágenes</span>')
    imagen_count.short_description = 'Imágenes'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('imagenes')

@admin.register(ImagenProyecto)
class ImagenProyectoAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'titulo', 'imagen_preview', 'orden', 'created_at']
    list_filter = ['proyecto', 'created_at']
    search_fields = ['proyecto__titulo', 'titulo', 'descripcion']
    list_editable = ['orden']
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    imagen_preview.short_description = 'Vista previa'

# Personalización del admin
admin.site.site_header = 'Administración del Currículum'
admin.site.site_title = 'Currículum Admin'
admin.site.index_title = 'Panel de Administración'
from django.db import models
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import os

class DatosPersonales(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Correo electrónico")
    descripcion = models.TextField(verbose_name="Descripción profesional")
    linkedin = models.URLField(blank=True, null=True, verbose_name="Perfil de LinkedIn")
    github = models.URLField(blank=True, null=True, verbose_name="Perfil de GitHub")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Datos Personales"
        verbose_name_plural = "Datos Personales"

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('desarrollo', 'En Desarrollo'),
        ('completado', 'Completado'),
        ('pausado', 'Pausado'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    titulo = models.CharField(max_length=100, verbose_name="Título del proyecto")
    descripcion = models.TextField(verbose_name="Descripción detallada")
    descripcion_corta = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Descripción corta",
        help_text="Descripción breve para mostrar en la vista principal"
    )
    link_github = models.URLField(blank=True, null=True, verbose_name="Enlace a GitHub")
    link_demo = models.URLField(blank=True, null=True, verbose_name="Enlace a demostración")
    
    # Campos de tecnologías organizados
    tecnologias = models.CharField(
        max_length=300, 
        blank=True, 
        null=True, 
        verbose_name="Tecnologías principales",
        help_text="Separar con comas (ej: Python, Django, PostgreSQL)"
    )
    frontend = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Tecnologías Frontend",
        help_text="Separar con comas (ej: React, Vue.js, HTML, CSS)"
    )
    backend = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Tecnologías Backend",
        help_text="Separar con comas (ej: Django, Node.js, Express)"
    )
    base_datos = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Base de datos",
        help_text="Separar con comas (ej: PostgreSQL, MongoDB, Redis)"
    )
    otras_librerias = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Otras librerías",
        help_text="Separar con comas (ej: TensorFlow, Pandas, JWT)"
    )
    
    # Campos adicionales
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='desarrollo',
        verbose_name="Estado del proyecto"
    )
    fecha_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de finalización")
    destacado = models.BooleanField(default=False, verbose_name="Proyecto destacado")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-destacado', 'orden', '-created_at']

    def __str__(self):
        return self.titulo
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin")
    
    @property
    def descripcion_display(self):
        """Retorna la descripción corta si existe, sino la descripción completa truncada"""
        if self.descripcion_corta:
            return self.descripcion_corta
        return self.descripcion[:150] + "..." if len(self.descripcion) > 150 else self.descripcion

class ImagenProyecto(models.Model):
    proyecto = models.ForeignKey(
        Proyecto, 
        related_name='imagenes', 
        on_delete=models.CASCADE,
        verbose_name="Proyecto"
    )
    imagen = models.ImageField(
        upload_to='proyectos/', 
        verbose_name="Imagen"
    )
    titulo = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Título de la imagen"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción de la imagen"
    )
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Proyecto"
        verbose_name_plural = "Imágenes de Proyectos"
        ordering = ['orden', 'created_at']

    def __str__(self):
        return f"Imagen de {self.proyecto.titulo}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.imagen:
            img = Image.open(self.imagen.path)
            
            # Configuración de tamaños
            max_width = 1200
            max_height = 800
            thumbnail_quality = 85
            
            # Redimensionar si es necesario
            if img.height > max_height or img.width > max_width:
                # Calcular el ratio para mantener la proporción
                ratio = min(max_width/img.width, max_height/img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Guardar la imagen optimizada
                img.save(self.imagen.path, quality=thumbnail_quality, optimize=True)
    
    def delete(self, *args, **kwargs):
        """Eliminar el archivo físico cuando se elimina el registro"""
        if self.imagen:
            if os.path.isfile(self.imagen.path):
                os.remove(self.imagen.path)
        super().delete(*args, **kwargs)
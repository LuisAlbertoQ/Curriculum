from django.db import models
from PIL import Image


class DatosPersonales(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    link_github = models.URLField(blank=True, null=True)
    tecnologias = models.CharField(max_length=200, blank=True, null=True)
    frontend = models.CharField(max_length=200, blank=True, null=True)
    backend = models.CharField(max_length=200, blank=True, null=True)
    base_datos = models.CharField(max_length=200, blank=True, null=True)
    otras_librerias = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.titulo

class ImagenProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='proyectos/')

    def __str__(self):
        return f"Imagen de {self.proyecto.titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la imagen primero

        img = Image.open(self.imagen.path)

        # Define el tamaño máximo (ajústalo a tu gusto)
        max_width = 100
        max_height = 100

        # Redimensiona manteniendo la relación de aspecto
        if img.height > max_height or img.width > max_width:
            img.thumbnail((max_width, max_height))
            img.save(self.imagen.path, quality=85, optimize=True)

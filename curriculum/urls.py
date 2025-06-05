# curriculum/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('proyecto/<int:proyecto_id>/', views.proyecto_detalle, name='proyecto_detalle'),
]

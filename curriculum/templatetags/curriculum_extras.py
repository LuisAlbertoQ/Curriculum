from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Divide una cadena por el separador especificado"""
    if value:
        return value.split(arg)
    return []

@register.filter
def trim(value):
    """Elimina espacios en blanco al inicio y final"""
    if value:
        return value.strip()
    return value
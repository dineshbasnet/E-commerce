from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the given value by the argument."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return ''
    
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to a form field"""
    return field.as_widget(attrs={'class': css_class})

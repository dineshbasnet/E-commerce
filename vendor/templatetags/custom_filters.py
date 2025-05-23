from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={"class": class_name})
    return value

from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    # Check if value is a form field (has 'as_widget' method)
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={"class": class_name})
    # If value is not a form field, return it as is
    return value

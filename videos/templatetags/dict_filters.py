from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    # Only access if d is a dictionary
    if isinstance(d, dict):
        return d.get(key)
    return None

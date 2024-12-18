from django import template

register = template.Library()

@register.filter
def active_path(request, pattern):
    return 'active' if request.path.startswith(pattern) else ''


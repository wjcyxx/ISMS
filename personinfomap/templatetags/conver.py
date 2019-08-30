from django import template
register = template.Library()

@register.filter
def conver_uuid(value):
    return ''.join(str(value).split('-'))
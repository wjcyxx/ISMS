from django import template
from basedata.models import base
from django.db.models import Q

register = template.Library()

@register.filter
def get_submenu(value):
    FPID = ''.join(str(value).split('-'))
    submenu_info = base.objects.filter(Q(FPID=FPID))
    return submenu_info


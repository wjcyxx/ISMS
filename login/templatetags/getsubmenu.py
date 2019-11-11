from django import template
from busmenu.models import busmenu
from django.db.models import Q

register = template.Library()

@register.filter
def get_submenu(value):
    FPID = ''.join(str(value).split('-'))
    submenu_info = busmenu.objects.filter(Q(FPID=FPID))
    return submenu_info


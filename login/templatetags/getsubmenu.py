from django import template
from busmenu.models import busmenu
from django.db.models import Q

register = template.Library()

@register.filter
def get_submenu(value):
    FPID = ''.join(str(value).split('-'))
    submenu_info = busmenu.objects.filter(Q(FPID=FPID), Q(FStatus=True)).order_by('FSequence')
    if submenu_info.count() == 0:
        return 0
    else:
        return submenu_info



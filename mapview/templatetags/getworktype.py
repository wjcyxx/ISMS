from django import template
from basedata.models import base
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter
def get_worktype(value):
    fid = ''.join(str(value).split('-'))

    try:
        worktype_name = base.objects.get(Q(FID=fid))

        return worktype_name.FBase
    except ObjectDoesNotExist:
        return  ''
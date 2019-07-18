from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from area.models import area
from basedata.models import base
from common.views import *
from django.http import JsonResponse
#from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist


def add(request):

    area_info = area.objects.all()
    resultdict = get_dict_transfer(area_info, 'FID', 'FName', 'FStatus')

    return render(request, "content/personauth/personauthadd.html", {'resultdict' : resultdict})

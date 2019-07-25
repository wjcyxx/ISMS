from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import hatrule as T_HatRule
from device.models import device
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from django.views.generic import View
# Create your views here.

class hatrule(EntranceView):

    EntranceView.template_name = 'content/hatrule/hatruleinfo.html'
    EntranceView.query_sets = [device.objects.filter(Q(FStatus=True))]
    EntranceView.quer_set_fieldnames = ['FDevice']


class get_datasourcea(get_datasource):

    def get_queryset(self, request):
        prjid = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FRule]", '')
        hatrule_info = T_HatRule.objects.filter(Q(CREATED_PRJ=prjid), Q(FRule__contains=serinput))

        return hatrule_info




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

    def set_context(self, request):
        dev_info = device.objects.filter(Q(FStatus=True))
        devinfo = get_dict_table(dev_info, 'FID', 'FDevice')

        context = {'device': devinfo}
        return  context


class get_datasourcea(get_datasource):

    def get_queryset(self, request):
        prjid = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FRule]", '')
        hatrule_info = T_HatRule.objects.filter(Q(CREATED_PRJ=prjid), Q(FRule__contains=serinput))

        return hatrule_info




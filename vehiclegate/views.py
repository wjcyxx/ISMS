from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import vehiclegate as T_VehicleGate
from device.models import device
from area.models import area
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/vehiclegate/vehiclegateinfo.html'
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FDevice', 'FName']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FGate]", '')
        vehiclegate_info =  T_VehicleGate.objects.filter(Q(CREATED_PRJ=prj_id), Q(FGate__contains=serinput))

        return vehiclegate_info


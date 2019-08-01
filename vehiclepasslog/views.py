from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from .models import vehiclepasslog as T_VehiclePassLog
from area.models import area
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from organize.models import organize
from basedata.models import base
# Create your views here.


#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/vehiclepasslog/vehiclepassloginfo.html'
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a'))
        ]
        self.quer_set_fieldnames = ['FName', 'FOrgname', 'FBase']


class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']

        self.type =1
        serinput = self.request.GET.get("resultdict[FPlate]", '')
        vehiclepasslog_info = T_VehiclePassLog.objects.filter(Q(CREATED_PRJ=prj_id), Q(FPlate__FPlate__contains=serinput)).values('FPlate', 'FGateID__FGate', 'FGateID__FAreaID', 'FGateID__FGatetype', 'FGateID__FGateattr', 'FPlate__FVehicletypeID', 'FPlate__FDrivers', 'FPlate__FOrgID', 'CREATED_TIME', 'FPicturepath')

        return vehiclepasslog_info


from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from .models import envalarmlog as T_EnvAlarmLog
from area.models import area
from common.views import *
from django.http import JsonResponse
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

        self.template_name = 'content/envalarmlog/envalarmloginfo.html'
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FName']


class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']

        self.type =1
        serinput = self.request.GET.get("resultdict[FRuleID__FRule]", '')
        envalarmlog_info =  T_EnvAlarmLog.objects.filter(Q(CREATED_PRJ=prj_id), Q(FRuleID__FRule__contains=serinput)).values('FRuleID__FRule', 'FDesc', 'FPortID__FPort', 'FPortID__FDriverdevice', 'FPortID__FStatus', 'FRuleID__FAreaID', 'CREATED_TIME')

        return envalarmlog_info


from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import dsps as T_MonitorPoint
from basedata.models import base
from device.models import device
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

        self.template_name = 'content/dsps/dspsinfo.html'
        self.query_sets = [
            base.objects.filter(Q(FPID='87fb4ac2c25d11e9b7e67831c1d24216')),
            device.objects.filter(Q(FStatus=True), Q(FDevtypeID='4d42f810c25f11e9b7e67831c1d24216'), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FBase', 'FDevice']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']

        serinput = self.request.GET.get("resultdict[FMonitor]", '')
        dsps_info = T_MonitorPoint.objects.filter(Q(CREATED_PRJ=prj_id), Q(FMonitor__contains=serinput))

        return dsps_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/dsps/dspsadd.html'
        self.objForm = DspsModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='87fb4ac2c25d11e9b7e67831c1d24216')),
            device.objects.filter(Q(FStatus=True), Q(FDevtypeID='4d42f810c25f11e9b7e67831c1d24216'), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FMonitortypeID', 'FDevID']
        self.query_set_valuefields = ['FBase', 'FDevice']


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/dsps/dspsadd.html'
        self.model = T_MonitorPoint
        self.objForm = DspsModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='87fb4ac2c25d11e9b7e67831c1d24216')),
            device.objects.filter(Q(FStatus=True), Q(FDevtypeID='4d42f810c25f11e9b7e67831c1d24216'), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FMonitortypeID', 'FDevID']
        self.query_set_valuefields = ['FBase', 'FDevice']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_MonitorPoint
        self.objForm = DspsModelForm

        self.query_sets = [
            base.objects.filter(Q(FPID='87fb4ac2c25d11e9b7e67831c1d24216')),
            device.objects.filter(Q(FStatus=True), Q(FDevtypeID='4d42f810c25f11e9b7e67831c1d24216'), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FMonitortypeID', 'FDevID']
        self.query_set_valuefields = ['FBase', 'FDevice']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_MonitorPoint




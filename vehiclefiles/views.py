from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import vehiclefiles as T_VehicleFiles
from device.models import device
from organize.models import organize
from basedata.models import base
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

        self.template_name = 'content/vehiclefiles/vehiclefilesinfo.html'
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a')),
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FOrgname', 'FBase', 'FDevice']

#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FPlate]", '')
        vehiclefiles_info =  T_VehicleFiles.objects.filter(Q(CREATED_PRJ=prj_id), Q(FPlate__contains=serinput))

        return vehiclefiles_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/vehiclefiles/vehiclefilesadd.html'
        self.objForm = VehicleFilesModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a')),
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FOrgID', 'FVehicletypeID', 'FDevID']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FDevice']


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/vehiclefiles/vehiclefilesadd.html'
        self.model = T_VehicleFiles
        self.objForm = VehicleFilesModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a')),
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FOrgID', 'FVehicletypeID', 'FDevID']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FDevice']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_VehicleFiles
        self.objForm = VehicleFilesModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a')),
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FOrgID', 'FVehicletypeID', 'FDevID']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FDevice']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_VehicleFiles

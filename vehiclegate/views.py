from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import vehiclegate as T_VehicleGate
from .models import vehiclesigin as T_VehicleSigin
from device.models import device
from area.models import area
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


#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/vehiclegate/vehiclegateadd.html'
        self.objForm = VehicleGateModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=self.request.session['PrjID'])),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']
        self.context['vehtype'] = 'null'

#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/vehiclegate/vehiclegateadd.html'
        self.model = T_VehicleGate
        self.objForm = VehicleGateModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=self.request.session['PrjID'])),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']

        vehicletype_info = get_dict_table(base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a')), 'FID', 'FBase')
        self.context['vehtype'] = vehicletype_info



#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_VehicleGate
        self.objForm = VehicleGateModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_VehicleGate


#链接新增通行策略模板
class add_sigin(add_base):
    def set_view(self, request):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/vehiclegate/vehiclesiginadd.html'
        self.objForm = VehicleSiginModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a'))
        ]
        self.query_set_idfields = ['FVehtypeID']
        self.query_set_valuefields = ['FBase']
        self.context['fid'] = fid



#返回控制策略数据table
class get_sigin_datasource(get_datasource_base):
    def get_queryset(self, reqeust):

        fid = self.request.GET.get('fid')

        vehiclesigin_info = T_VehicleSigin.objects.filter(Q(FPID=fid))
        return vehiclesigin_info


#处理通行策略新增及保存数据
class insert_sigin(insert_base):
    def set_view(self, request):
        self.model = T_VehicleSigin
        self.objForm = VehicleSiginModelForm
        self.type = 1
        self.query_sets = [
            base.objects.filter(Q(FPID='571076ccb39311e98ed5708bcdb9b39a'))
        ]
        self.query_set_idfields = ['FVehtypeID']
        self.query_set_valuefields = ['FBase']


#处理控制策略删除
class delete_sigin(delete_base):
    def set_view(self,request):
        self.model = T_VehicleSigin


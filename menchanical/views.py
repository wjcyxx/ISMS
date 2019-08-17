from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import menchanical as T_Menchanical
from .models import mecoperauth as T_MecOperAuth
from .models import mecoperlog as T_MecOperLog
from device.models import device
from basedata.models import base
from personnel.models import personnel
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

        self.template_name = 'content/menchanical/menchanicalinfo.html'
        self.query_sets = [
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id),Q(FDevtypeID='af2cecf8bd6811e987267831c1d24216')),
            base.objects.filter(Q(FPID='a7541a6abd7211e9a59c7831c1d24216')),
            personnel.objects.filter(Q(FStatus=0), Q(CREATED_PRJ=prj_id), Q(FSpecialequ=True))
        ]
        self.quer_set_fieldnames = ['FDevice', 'FBase', 'FName']

#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FMecspec]", '')
        mench_info = T_Menchanical.objects.filter(Q(CREATED_PRJ=prj_id), Q(FMecspec__contains=serinput))

        return mench_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/menchanical/menchanicaladd.html'
        self.objForm = MenchModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id), Q(FDevtypeID='af2cecf8bd6811e987267831c1d24216')),
            base.objects.filter(Q(FPID='a7541a6abd7211e9a59c7831c1d24216'))
        ]
        self.query_set_idfields = ['FMonitordevID', 'FMectypeID']
        self.query_set_valuefields = ['FDevice', 'FBase']


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/menchanical/menchanicaladd.html'
        self.model = T_Menchanical
        self.objForm = MenchModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id), Q(FDevtypeID='af2cecf8bd6811e987267831c1d24216')),
            base.objects.filter(Q(FPID='a7541a6abd7211e9a59c7831c1d24216'))
        ]
        self.query_set_idfields = ['FMonitordevID', 'FMectypeID']
        self.query_set_valuefields = ['FDevice', 'FBase']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_Menchanical
        self.objForm = MenchModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id), Q(FDevtypeID='af2cecf8bd6811e987267831c1d24216')),
            base.objects.filter(Q(FPID='a7541a6abd7211e9a59c7831c1d24216'))
        ]
        self.query_set_idfields = ['FMonitordevID', 'FMectypeID']
        self.query_set_valuefields = ['FDevice', 'FBase']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_Menchanical


#链接添加操作人员权限模板
class add_auth(add_base):
    def set_view(self, request):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/menchanical/mecoperauthadd.html'
        self.objForm = MecOperAuthModelForm
        self.query_sets = [
            personnel.objects.filter(Q(FStatus=0), Q(CREATED_PRJ=prj_id), Q(FSpecialequ=True))
        ]
        self.query_set_idfields = ['FAuthpersonID']
        self.query_set_valuefields = ['FName']
        self.context['fid'] = fid


#处理操作授权新增及保存数据
class insert_auth(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_MecOperAuth
        self.objForm = MecOperAuthModelForm
        self.type = 1
        self.query_sets = [
            personnel.objects.filter(Q(FStatus=0), Q(CREATED_PRJ=prj_id), Q(FSpecialequ=True))
        ]
        self.query_set_idfields = ['FAuthpersonID']
        self.query_set_valuefields = ['FName']


#返回操作授权table数据及查询结果
class get_operauth_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        auth_info = T_MecOperAuth.objects.filter(Q(FPID=fid))
        return auth_info


#返回操作记录table数据及查询结果
class get_operlog_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        operlog_info = T_MecOperLog.objects.filter(FMecserialFID=fid)
        return operlog_info



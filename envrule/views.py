from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import envrule as T_Envrule
from .models import envruleswitch as T_EnvRuleSwitch
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

        self.template_name = 'content/envrule/envruleinfo.html'
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FDevice', 'FName']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FRule]", '')
        envrule_info =  T_Envrule.objects.filter(Q(CREATED_PRJ=prj_id), Q(FRule__contains=serinput))

        return envrule_info


#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/envrule/envruleadd.html'
        self.objForm = EnvRuleModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']

#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/envrule/envruleadd.html'
        self.model = T_Envrule
        self.objForm = EnvRuleModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_Envrule
        self.objForm = EnvRuleModelForm
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_Envrule


#链接新增控制策略模板
class add_switch(add_base):
    def set_view(self, request):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/envrule/envruleswitchadd.html'
        self.objForm = EnvRuleSwitchModelForm
        self.context['fid'] = fid

#返回控制策略数据table
class get_switch_datasource(get_datasource_base):
    def get_queryset(self, reqeust):

        fid = self.request.GET.get('fid')

        envruleswitch_info = T_EnvRuleSwitch.objects.filter(Q(FPID=fid))
        return envruleswitch_info



#处理控制策略新增及保存
class insert_switch(insert_base):
    def set_view(self, request):

        self.model = T_EnvRuleSwitch
        self.objForm = EnvRuleSwitchModelForm
        self.type = 1


#处理控制策略删除
class delete_switch(delete_base):
    def set_view(self,request):
        self.model = T_EnvRuleSwitch
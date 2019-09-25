from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import monitordev as T_MonitorDev
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

        self.template_name = 'content/monitordev/monitordevinfo.html'
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FName']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FChannel]", '')
        monitordev_info = T_MonitorDev.objects.filter(Q(CREATED_PRJ=prj_id), Q(FChannel__contains=serinput))

        return monitordev_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/monitordev/monitordevadd.html'
        self.objForm = MonitorDevModelForm
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FAreaID']
        self.query_set_valuefields = ['FName']


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/monitordev/monitordevadd.html'
        self.model = T_MonitorDev
        self.objForm = MonitorDevModelForm
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FAreaID']
        self.query_set_valuefields = ['FName']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_MonitorDev
        self.objForm = MonitorDevModelForm
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.query_set_idfields = ['FAreaID']
        self.query_set_valuefields = ['FName']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_MonitorDev




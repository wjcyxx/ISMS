from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import safetrain as T_SafeTrain
from .models import safetrainperson as T_SafeTrainPerson
from personnel.models import personnel
from team.models import team
from group.models import group
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
        self.template_name = 'content/safetrain/safetraininfo.html'
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a'))
        ]
        self.quer_set_fieldnames = ['FBase']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FSubject]", '')
        safetrain_info =  T_SafeTrain.objects.filter(Q(CREATED_PRJ=prj_id), Q(FSubject__contains=serinput))

        return safetrain_info


#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/safetrain/safetrainadd.html'
        self.objForm = SafeTrainModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.query_set_idfields = ['FTraintypeID']
        self.query_set_valuefields = ['FBase']


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/safetrain/safetrainadd.html'
        self.model = T_SafeTrain
        self.objForm = SafeTrainModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.query_set_idfields = ['FTraintypeID']
        self.query_set_valuefields = ['FBase']



#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_SafeTrain
        self.objForm = SafeTrainModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.query_set_idfields = ['FTraintypeID']
        self.query_set_valuefields = ['FBase']


#选择工人页面入口
class selperson(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/safetrain/selpersoninfo.html'
        self.query_sets = [
            team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
        ]
        self.quer_set_fieldnames = ['FName', 'FGroup', 'FBase']


#返回选择工人table数据及查询结果
class get_selperson_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FName]", '')
        person_info =  personnel.objects.filter(Q(CREATED_PRJ=prj_id), Q(FName__contains=serinput))

        return person_info



class insert_person(View):
    def post(self, request):
        pass

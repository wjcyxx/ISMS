from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import mencrepairplan as T_MencRepairPlan
from basedata.models import base
from menchanical.models import menchanical
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
        self.template_name = 'content/mencrepairplan/mencrepairplaninfo.html'
        self.query_sets = [
            base.objects.filter(Q(FPID='a7541a6abd7211e9a59c7831c1d24216')),
        ]
        self.quer_set_fieldnames = ['FBase']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FMecserialFID__FMecserialID]", '')
        self.type = 1
        repairplan_info = T_MencRepairPlan.objects.filter(Q(CREATED_PRJ=prj_id), Q(FMecserialFID__FMecserialID__contains=serinput)).values('FID', 'FMecserialFID__FMecserialID', 'FMecserialFID__FMectypeID','FMecserialFID__FMecspec', 'FChecktype', 'FInterval', 'FFirstcheckdate', 'FStatus', 'FDesc')

        return repairplan_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/mencrepairplan/mencrepairplanadd.html'
        self.objForm = MencRepairPlanModelForm

        arr_id = []
        mencserial_info = T_MencRepairPlan.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        if mencserial_info.count() > 0:
            for obj in mencserial_info:
                str_id = ''.join(str(obj.FMecserialFID_id).split('-'))
                arr_id.append(str_id)


        mench_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id), ~Q(FID__in=arr_id))
        self.context['mench'] =  mench_info
        self.context['mencSerial'] = 'null'


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/mencrepairplan/mencrepairplanadd.html'
        self.model = T_MencRepairPlan
        self.objForm = MencRepairPlanModelForm

        mench_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        self.context['mench'] =  mench_info

        mencSerial = T_MencRepairPlan.objects.get(Q(FID=fid)).FMecserialFID_id
        self.context['mencSerial'] = mencSerial


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_MencRepairPlan
        self.objForm = MencRepairPlanModelForm

        self.set_fields = ['FMecserialFID_id']
        self.set_value = [self.request.POST.get('FMecserialFID')]


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_MencRepairPlan



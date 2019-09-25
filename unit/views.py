from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import unit as T_Unit
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
        self.template_name = 'content/unit/unitinfo.html'
        self.query_sets = [
            base.objects.filter(Q(FPID='32364d5cb67e11e9b11d7831c1d24216'))
        ]
        self.quer_set_fieldnames = ['FBase']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        serinput = self.request.GET.get("resultdict[FUnit]", '')
        unit_info =  T_Unit.objects.filter(Q(FUnit__contains=serinput))

        return unit_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/unit/unitadd.html'
        self.objForm = UnitModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='32364d5cb67e11e9b11d7831c1d24216'))
        ]
        self.query_set_idfields = ['FUnitgroupID']
        self.query_set_valuefields = ['FBase']


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/unit/unitadd.html'
        self.model = T_Unit
        self.objForm = UnitModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='32364d5cb67e11e9b11d7831c1d24216'))
        ]
        self.query_set_idfields = ['FUnitgroupID']
        self.query_set_valuefields = ['FBase']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_Unit
        self.objForm = UnitModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='32364d5cb67e11e9b11d7831c1d24216'))
        ]
        self.query_set_idfields = ['FUnitgroupID']
        self.query_set_valuefields = ['FBase']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_Unit

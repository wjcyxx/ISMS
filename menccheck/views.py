from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import menccheck as T_MencCheck
from menchanical.models import menchanical
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

        self.template_name = 'content/menccheck/menccheckinfo.html'
        self.query_sets = [
            base.objects.filter(Q(FPID='a7541a6abd7211e9a59c7831c1d24216')),
            personnel.objects.filter(Q(FStatus=0), Q(CREATED_PRJ=prj_id), Q(FSpecialequ=True))
        ]
        self.quer_set_fieldnames = ['FBase', 'FName']
        checkItem = base.objects.filter(FPID='3c88127abf5e11e983587831c1d24216')
        self.context['checkItem'] = get_dict_table(checkItem, 'FID', 'FBase')



#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FMecserialFID__FMecserialID]", '')
        self.type = 1
        menccheck_info = T_MencCheck.objects.filter(Q(CREATED_PRJ=prj_id), Q(FMecserialFID__FMecserialID__contains=serinput)).values('FID', 'FMecserialFID__FMecserialID', 'FMecserialFID__FMectypeID','FMecserialFID__FMecspec', 'FCheckPersonID', 'FCheckitemID', 'FCheckresult', 'FCheckdate')

        return menccheck_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/menccheck/menccheckadd.html'
        self.objForm = MencCheckModelForm
        self.query_sets = [
            personnel.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=0)),
            base.objects.filter(Q(FPID='3c88127abf5e11e983587831c1d24216'))
        ]
        self.query_set_idfields = ['FCheckPersonID', 'FCheckitemID']
        self.query_set_valuefields = ['FName', 'FBase']

        mench_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        self.context['mench'] =  mench_info
        self.context['mencSerial'] = 'null'


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/menccheck/menccheckadd.html'
        self.model = T_MencCheck
        self.objForm = MencCheckModelForm
        self.query_sets = [
            personnel.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=0)),
            base.objects.filter(Q(FPID='3c88127abf5e11e983587831c1d24216'))
        ]
        self.query_set_idfields = ['FCheckPersonID', 'FCheckitemID']
        self.query_set_valuefields = ['FName', 'FBase']

        mench_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        self.context['mench'] =  mench_info

        mencSerial = T_MencCheck.objects.get(Q(FID=fid)).FMecserialFID_id
        self.context['mencSerial'] = mencSerial


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_MencCheck
        self.objForm = MencCheckModelForm
        self.query_sets = [
            personnel.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=0)),
            base.objects.filter(Q(FPID='3c88127abf5e11e983587831c1d24216'))
        ]
        self.query_set_idfields = ['FCheckPersonID', 'FCheckitemID']
        self.query_set_valuefields = ['FName', 'FBase']

        self.set_fields = ['FMecserialFID_id']
        self.set_value = [self.request.POST.get('FMecserialFID')]



from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import materialsaccount as T_MaterialAccount
from .models import materaccountgoods as T_MaterialAccountGoods
from organize.models import organize
from materials.models import materials
from project.models import project
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

        self.template_name = 'content/receaccount/receaccountinfo.html'
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            materials.objects.filter(Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FOrgname', 'FBase', 'FName']

#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FPID__FPoundNo]", '')
        self.type = 1

        receaccount_info = T_MaterialAccountGoods.objects.filter(Q(FPID__CREATED_PRJ=prj_id), Q(FPID__FPoundNo__contains=serinput), Q(FPID__FReceivetype=0)).values('FPID__FID', 'FPID__FPoundNo', 'FPID__FPlate', 'FPID__FOperationalOrgID','FPID__FWorktypeID', 'FMaterID', 'FPID__CREATED_TIME','FWaybillQty', 'FConfirmQty', 'FDeviationQty', 'FPID__FStatus')

        return receaccount_info


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/receaccount/receaccountadd.html'
        self.model = T_MaterialAccount
        self.objForm = ReceAccountModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            project.objects.filter(Q(FStatus=True))
        ]
        self.query_set_idfields = ['FOperationalOrgID', 'FWorktypeID', 'CREATED_PRJ']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FPrjname']

#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_MaterialAccount
        self.objForm = ReceAccountModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            project.objects.filter(Q(FStatus=True))
        ]
        self.query_set_idfields = ['FOperationalOrgID', 'FWorktypeID', 'CREATED_PRJ']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FPrjname']



#返回原始运单信息table
class get_originbill_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        originbill_info = T_MaterialAccount.objects.filter(Q(FID=fid))
        return  originbill_info

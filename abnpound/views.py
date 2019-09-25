from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q, F
from receaccount.models import materialsaccount as T_MaterialAccount
from receaccount.models import materaccountgoods as T_MaterialAccountGoods
from .models import abnpound as T_AbnormalPound
from organize.models import organize
from materials.models import materials
from project.models import project
from basedata.models import base
from goodstype.models import goodstype
from unit.models import unit
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

        self.template_name = 'content/abnpound/abnpoundinfo.html'
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            materials.objects.filter(Q(CREATED_PRJ=prj_id)),
            unit.objects.filter(Q(FStatus=True))
        ]
        self.quer_set_fieldnames = ['FOrgname', 'FBase', 'FName', 'FUnit']

#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FPID__FPoundNo]", '')
        self.type = 1

        receaccount_info = T_MaterialAccountGoods.objects.filter(Q(FPID__CREATED_PRJ=prj_id), Q(FPID__FPoundNo__contains=serinput), Q(FPID__FReceivetype=0), (Q(FPID__FStatus=0) | Q(FPID__FStatus=1)), (Q(FDeviationQty__lte=F('FMaterID__FNegativeDeviation')))).values('FPID__FID', 'FPID__FPoundNo', 'FPID__FPlate', 'FPID__FOperationalOrgID','FPID__FWorktypeID', 'FMaterID__FName', 'FPID__F1stWeighTime', 'FPID__F2ndWeighTime', 'FPID__F1stWeigh', 'FPID__F2ndWeigh', 'FPID__CREATED_TIME','FWaybillQty', 'FConfirmQty', 'FDeviationQty', 'FUnitID', 'FPID__FStatus')

        return receaccount_info

#链接新增模板
class add(add_base):
    def set_view(self, request):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/abnpound/abnpoundadd.html'
        self.objForm = AbnPoundModelForm

        recepound_info = T_MaterialAccount.objects.get(Q(FID=fid))
        self.context['PoundNo'] = recepound_info.FPoundNo
        self.context['ResultDate'] = timezone.now().strftime('%Y-%m-%d')
        self.context['FPID'] = fid


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_AbnormalPound
        self.objForm = AbnPoundModelForm

        self.set_fields = ['FPoundID']
        self.set_value = [self.request.POST.get('FPID')]


    def set_view_aftersave(self, request):
        fid = self.request.POST.get('FPID')
        result = self.request.POST.get('FResult')
        i = 0

        if result == '0':
            i = 5
        elif result == '1':
            i = 4
        elif result == '2':
            i = 3

        T_MaterialAccount.objects.filter(Q(FID=fid)).update(FStatus=i)



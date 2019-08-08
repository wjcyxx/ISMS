from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from receaccount.models import materialsaccount as T_MaterialAccount
from receaccount.models import materaccountgoods as T_MaterialAccountGoods
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

        self.template_name = 'content/recepound/recepoundinfo.html'
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

        receaccount_info = T_MaterialAccountGoods.objects.filter(Q(FPID__CREATED_PRJ=prj_id), Q(FPID__FPoundNo__contains=serinput), Q(FPID__FReceivetype=0), ~Q(FPID__FStatus=2)).values('FPID__FID', 'FPID__FPoundNo', 'FPID__FPlate', 'FPID__FOperationalOrgID','FPID__FWorktypeID', 'FMaterID__FName', 'FPID__CREATED_TIME','FWaybillQty', 'FConfirmQty', 'FDeviationQty', 'FPID__FStatus')

        return receaccount_info


#链接新增模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/recepound/recepoundadd.html'
        self.objForm = RecePoundModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            project.objects.filter(Q(FStatus=True))
        ]
        self.query_set_idfields = ['FOperationalOrgID', 'FWorktypeID', 'CREATED_PRJ']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FPrjname']

        prefix = timezone.now().strftime("%Y%m%d")
        pound_no = gensequence('recepound', prefix, 4, 1)
        self.context['poundNo'] = pound_no


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/recepound/recepoundadd.html'
        self.model = T_MaterialAccount
        self.objForm = RecePoundModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            project.objects.filter(Q(FStatus=True))
        ]
        self.query_set_idfields = ['FOperationalOrgID', 'FWorktypeID', 'CREATED_PRJ']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FPrjname']

        goodstype_info = get_dict_table(goodstype.objects.filter(Q(FPID__isnull=False)), 'FID', 'FGoodsType')
        unit_info = get_dict_table(unit.objects.filter(Q(FStatus=True)), 'FID', 'FUnit')
        self.context['goodstype'] = goodstype_info
        self.context['unit'] = unit_info

        id = ''.join(str(self.request.GET.get('fid')).split('-'))
        receaccount = T_MaterialAccount.objects.get(Q(FID=id))
        self.context['inpic1'] = str(receaccount.FInPicpath1)
        self.context['outpic1'] = str(receaccount.FOutPicpath1)


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_MaterialAccount
        self.objForm = RecePoundModelForm
        self.query_sets = [
            organize.objects.filter(Q(FStatus=True)),
            base.objects.filter(Q(FPID='d8cb4a18b81911e999f07831c1d24216')),
            project.objects.filter(Q(FStatus=True)),
        ]
        self.query_set_idfields = ['FOperationalOrgID', 'FWorktypeID', 'CREATED_PRJ']
        self.query_set_valuefields = ['FOrgname', 'FBase', 'FPrjname']

        self.set_fields = ['FReceivetype']
        self.set_value = [0]

    def set_view_aftersave(self, request):
        fpid = self.request.POST.get('FID')
        recpound_info = T_MaterialAccount.objects.get(FID=fpid)

        recepoundgoods_info =  T_MaterialAccountGoods.objects.create(FPID=recpound_info)
        #recepoundgoods_info.FPID = recpound_info.FID
        recepoundgoods_info.CREATED_PRJ = self.request.session['PrjID']
        recepoundgoods_info.CREATED_ORG = self.request.session['UserOrg']
        recepoundgoods_info.CREATED_BY = self.request.session['UserID']
        recepoundgoods_info.UPDATED_BY = self.request.session['UserID']
        recepoundgoods_info.CREATED_TIME = timezone.now()
        recepoundgoods_info.save()


#返回原始运单信息table
class get_originbill_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        originbill_info = T_MaterialAccount.objects.filter(Q(FID=fid))
        return  originbill_info


#返回材料明细信息table
class get_material_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.type = 1
        material_info = T_MaterialAccountGoods.objects.filter(Q(FPID=fid)).values('FMaterID__FMaterID', 'FMaterID__FName', 'FMaterID__FGoodsTypeID', 'FMaterID__FSpec', 'FMaterID__FUnitID', 'FMaterID__FTexture', 'FWaybillQty', 'FConfirmQty', 'FDeviationQty')
        return material_info


#处理作废
class recevoid(disabled_base):
    def set_view(self, request):
        self.model = T_MaterialAccount
        self.type = 1
        self.status = [3,2]


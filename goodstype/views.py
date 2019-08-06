from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import goodstype as T_GoodsType
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
        self.template_name = 'content/goodstype/goodstypeinfo.html'


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FGoodsType]", '')
        goodstype_info =  T_GoodsType.objects.filter(Q(CREATED_PRJ=prj_id), Q(FGoodsType__contains=serinput), Q(FPID__isnull=True))

        return goodstype_info


#链接增加模板
class add(add_base):
    def set_view(self, request):

        self.template_name = 'content/goodstype/goodstypeadd.html'
        self.objForm = GoosTypeModelForm

#链接编辑模板
class edit(edit_base):
    def set_view(self, request):

        self.template_name = 'content/goodstype/goodstypeadd.html'
        self.model = T_GoodsType
        self.objForm = GoosTypeModelForm

#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_GoodsType
        self.objForm = GoosTypeModelForm

#处理删除大类
class delete(delete_base):
    def set_view(self,request):
        fid = ''.join(str(self.request.POST.get('fid')).split('-'))
        self.model = T_GoodsType

        if T_GoodsType.objects.filter(Q(FPID=fid)).count() > 0:
            self.response_data['result'] = '2'
            self.response_data['message'] = '该大类下有子类明细，不允许删除'



#链接新增物料子类模板
class add_subtype(add_base):
    def set_view(self, request):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/goodstype/goodssubtypeadd.html'
        self.objForm = SubTypeModelForm
        self.query_sets = [
            T_GoodsType.objects.filter(Q(FPID__isnull=True))
        ]
        self.query_set_idfields = ['FPID']
        self.query_set_valuefields = ['FGoodsType']

        self.context['fid'] = fid

#返回物料子类数据table
class get_subtype_datasource(get_datasource_base):
    def get_queryset(self, reqeust):

        fid = self.request.GET.get('fid')

        subtype_info = T_GoodsType.objects.filter(Q(FPID=fid))
        return subtype_info


#处理物料子类新增及保存
class insert_subtype(insert_base):
    def set_view(self, request):
        self.model = T_GoodsType
        self.objForm = SubTypeModelForm
        self.query_sets = [
            T_GoodsType.objects.filter(Q(FPID__isnull=True))
        ]
        self.query_set_idfields = ['FPID']
        self.query_set_valuefields = ['FGoodsType']

        self.type = 1


#处理物料子类删除
class delete_subtype(delete_base):
    def set_view(self,request):
        self.model = T_GoodsType

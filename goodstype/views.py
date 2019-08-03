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
        goodstype_info =  T_GoodsType.objects.filter(Q(CREATED_PRJ=prj_id), Q(FGoodsType__contains=serinput))

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


#链接新增物料子类模板
class add_switch(add_base):
    def set_view(self, request):
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/goodstype/goodssubtypeadd.html'
        #self.objForm = EnvRuleSwitchModelForm
        self.context['fid'] = fid

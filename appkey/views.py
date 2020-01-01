from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import appkey as T_AppKey
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
        self.template_name = 'content/appkey/appkeyinfo.html'


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        self.orgsplit_type = 1
        serinput = self.request.GET.get("resultdict[FAppName]", '')
        appkey_info =  T_AppKey.objects.filter(Q(FAppName__contains=serinput), Q(FType=0) | Q(CREATED_PRJ=prj_id))

        return appkey_info

#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/appkey/appkeyadd.html'
        self.objForm = AppKeyModelForm


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/appkey/appkeyadd.html'
        self.model = T_AppKey
        self.objForm = AppKeyModelForm


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_AppKey
        self.objForm = AppKeyModelForm

        if self.request.GET.get('actype') == 'insert':
            if self.request.POST.get('FType') == 0:
                appkey = get_Random_String(10)
                self.set_fields = ['FAppkey']
                self.set_value = [appkey]


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_AppKey


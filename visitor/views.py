from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import visitor as T_Visitor
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

        self.template_name = 'content/visitor/visitorinfo.html'


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FName]", '')
        visitor_info =  T_Visitor.objects.filter(Q(CREATED_PRJ=prj_id), Q(FName__contains=serinput))

        return visitor_info


#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/visitor/visitoradd.html'
        self.objForm = VisitorModelForm

#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/visitor/visitoradd.html'
        self.model = T_Visitor
        self.objForm = VisitorModelForm


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_Visitor
        self.objForm = VisitorModelForm

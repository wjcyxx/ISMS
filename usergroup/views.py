from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import usergroup as T_UserGroup
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
        self.template_name = 'content/usergroup/usergroupinfo.html'


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        serinput = self.request.GET.get("resultdict[FName]", '')
        usergroup_info = T_UserGroup.objects.filter(Q(FName__contains=serinput))

        return usergroup_info


#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/usergroup/usergroupadd.html'
        self.objForm = UserGroupModelForm

#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/usergroup/usergroupadd.html'
        self.model = T_UserGroup
        self.objForm = UserGroupModelForm


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_UserGroup
        self.objForm = UserGroupModelForm
        


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_UserGroup

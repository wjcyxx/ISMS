from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import busmenu as T_Menu
from unit.models import unit
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from .forms import *
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/busmenu/busmenuinfo.html'

#返回menutree数据
class get_treedatasource(View):
    def post(self, request):

        obj_arr = []
        menu_info = T_Menu.objects.all()
        #menu_info = org_split(menu_info, request).order_by('FSequence')

        for obj in menu_info:
            dict = {}
            dict['id'] = ''.join(str(obj.FID).split('-'))
            dict['title'] = obj.FMenuName
            if obj.FPID == None or obj.FPID == '':
                dict['parentId'] = '0'
            else:
                dict['parentId'] = obj.FPID
                dict['iconClass'] = 'dtree-icon-sort'

            obj_arr.append(dict)

        resultdict = {"status":{"code":200,"message":"操作成功"}, "data": obj_arr}

        return JsonResponse(resultdict, safe=False)


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        serinput = self.request.GET.get("resultdict[FMenuName]", '')
        menu_info =  T_Menu.objects.filter(Q(FMenuName__contains=serinput)).order_by('FMenuPosition', 'FSequence')

        return menu_info

#返回点击菜单节点刷新数据结果
class get_refdatasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid = self.request.GET.get('fid')
        fpid = self.request.GET.get('fpid')

        if fpid != '0':
            menu_info =  T_Menu.objects.filter(Q(FID=fid)).order_by('FSequence')
        else:
            arr_id = []

            menu_info =  T_Menu.objects.filter(Q(FPID=fid)).order_by('FSequence')

        return menu_info


#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/busmenu/busmenuadd.html'
        node_id = self.request.GET.get('nodeid')
        node_pid = self.request.GET.get('nodepid')

        self.objForm = BusMenuModelForm
        self.query_sets = [
            T_Menu.objects.all().order_by('FSequence')
        ]
        self.query_set_idfields = ['FPID']
        self.query_set_valuefields = ['FMenuName']
        self.context['node_id'] = node_id
        self.context['node_pid'] = node_pid

#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/busmenu/busmenuadd.html'
        self.model = T_Menu
        self.objForm = BusMenuModelForm
        self.query_sets = [
            T_Menu.objects.all().order_by('FSequence')
        ]
        self.query_set_idfields = ['FPID']
        self.query_set_valuefields = ['FMenuName']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_Menu
        self.objForm = BusMenuModelForm
        self.query_sets = [
            T_Menu.objects.all(),
        ]
        self.query_set_idfields = ['FPID']
        self.query_set_valuefields = ['FMenuName']


#处理禁用/启用
class disabled(disabled_base):
    def set_view(self, request):
        self.model = T_Menu


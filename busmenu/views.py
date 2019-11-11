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
        menu_info = org_split(menu_info, request).order_by('FSequence')

        for obj in menu_info:
            dict = {}
            dict['id'] = ''.join(str(obj.FID).split('-'))
            dict['title'] = obj.FMenuName
            if obj.FPID == None:
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
        menu_info =  T_Menu.objects.filter(Q(FMenuName__contains=serinput))

        return menu_info


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

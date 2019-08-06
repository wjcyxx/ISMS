from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import materials as T_Materials
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

        self.template_name = 'content/materials/materialsinfo.html'
        self.query_sets = [
            goodstype.objects.filter(Q(CREATED_PRJ=prj_id),Q(FPID__isnull=False)),
            unit.objects.all()
        ]
        self.quer_set_fieldnames = ['FGoodsType', 'FUnit']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FName]", '')
        materials_info =  T_Materials.objects.filter(Q(CREATED_PRJ=prj_id), Q(FName__contains=serinput))

        return materials_info


class get_refdatasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        fid = self.request.GET.get('fid')
        fpid = self.request.GET.get('fpid')

        if fpid != '0':
            materials_info =  T_Materials.objects.filter(Q(CREATED_PRJ=prj_id), Q(FGoodsTypeID=fid))
        else:
            arr_id = []

            goodstype_info = goodstype.objects.filter(Q(FPID=fid))
            if goodstype_info.count() > 0:

                for obj in goodstype_info:
                    str_id = ''.join(str(obj.FID).split('-'))
                    arr_id.append(str_id)

            materials_info =  T_Materials.objects.filter(Q(CREATED_PRJ=prj_id), Q(FGoodsTypeID__in=arr_id))


        return materials_info


#返回物料类型tree数据
class get_treedatasource(View):
    def get(self, request):
        pass

    def post(self, request):
        prj_id = request.session['PrjID']

        obj_arr = []

        goodstype_info = goodstype.objects.filter(Q(CREATED_PRJ=prj_id))

        for obj in goodstype_info:
            dict = {}
            dict['id'] = ''.join(str(obj.FID).split('-'))
            dict['title'] = obj.FGoodsType
            if obj.FPID == None:
                dict['parentId'] = '0'
            else:
                dict['parentId'] = obj.FPID
                dict['iconClass'] = 'dtree-icon-sort'

            obj_arr.append(dict)

        resultdict = {"status":{"code":200,"message":"操作成功"}, "data": obj_arr}

        return JsonResponse(resultdict, safe=False)


#链接增加模板
class add(add_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/materials/materialsadd.html'
        self.objForm = MaterialsModelForm
        self.query_set_idfields = ['FGoodsTypeID', 'FUnitID']
        self.query_set_valuefields = ['FGoodsType', 'FUnit']

        if self.request.GET.get('nodepid') == '0':
            self.query_sets = [
                goodstype.objects.filter(Q(CREATED_PRJ=prj_id),Q(FPID=self.request.GET.get('nodeid'))),
                unit.objects.all()
            ]
            self.context['GoodsType_ID'] = 'null'
        else:
            self.query_sets = [
                goodstype.objects.filter(Q(CREATED_PRJ=prj_id),Q(FPID__isnull=False)),
                unit.objects.all()
            ]
            self.context['GoodsType_ID'] = self.request.GET.get('nodeid')


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/materials/materialsadd.html'
        self.model = T_Materials
        self.objForm = MaterialsModelForm
        self.query_sets = [
            goodstype.objects.filter(Q(CREATED_PRJ=prj_id),Q(FPID__isnull=False)),
            unit.objects.all()
        ]
        self.query_set_idfields = ['FGoodsTypeID', 'FUnitID']
        self.query_set_valuefields = ['FGoodsType', 'FUnit']


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.model = T_Materials
        self.objForm = MaterialsModelForm
        self.query_sets = [
            goodstype.objects.filter(Q(CREATED_PRJ=prj_id),Q(FPID__isnull=False)),
            unit.objects.all()
        ]
        self.query_set_idfields = ['FGoodsTypeID', 'FUnitID']
        self.query_set_valuefields = ['FGoodsType', 'FUnit']

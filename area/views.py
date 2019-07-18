from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import area as T_Area
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#区域管理控制器入口
def area(request):

    return render(request, 'content/area/areainfo.html')

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FName]", '')

    prj_id = request.session['PrjID']

    Area_info =  T_Area.objects.filter(Q(FName__contains=serinput), Q(CREATED_PRJ=prj_id))
    dict = convert_to_dicts(Area_info)
    resultdict = {'code':0, 'msg':"", 'count': Area_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#链接增加模板
def add(request):
    obj = AreaModelForm()

    return render(request, "content/area/areaadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Area_info = T_Area.objects.get(Q(FID=fid))
    obj = AreaModelForm(instance=Area_info)

    return render(request, "content/area/areaadd.html", {'obj': obj, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = AreaModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Area_info = T_Area.objects.get(FID=fid)
            obj = AreaModelForm(request.POST, instance=Area_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                if request.GET.get('actype') == 'insert':
                    temp.FStatus = True
                    temp.FIsCheckworkatten = True
                temp.CREATED_PRJ = request.session['PrjID']
                temp.CREATED_ORG = request.session['UserOrg']
                temp.CREATED_BY = request.session['UserID']
                temp.UPDATED_BY = request.session['UserID']
                temp.CREATED_TIME = timezone.now()

                temp.save()
                response_data['result'] = '0'
            else:
                response_data['msg'] = obj.errors
                response_data['result'] = '1'

            return HttpResponse(json.dumps(response_data))

        except Exception as e:
            response_data['msg'] = e
            response_data['result'] = '1'

            return HttpResponse(json.dumps(response_data))

#处理禁用/启用区域
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Area_info = T_Area.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Area_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Area_info.FStatus = True

            Area_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))

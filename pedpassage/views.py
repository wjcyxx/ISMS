from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import pedpassage as T_PedPassage
from device.models import device
from area.models import area
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
#设备管理控制器入口
def pedpassage(request):
    prjid = request.session['PrjID']

    device_info = device.objects.filter(Q(FStatus=True))
    area_info = area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prjid))

    deviceinfo = get_dict_table(device_info, 'FID', 'FDevice')
    areainfo = get_dict_table(area_info, 'FID', 'FName')

    return render(request, 'content/pedpassage/pedpassageinfo.html', {'deviceinfo': deviceinfo, 'areainfo': areainfo})


#返回table数据及查询结果
def get_datasource(request):

    prjid = request.session['PrjID']
    serinput = request.POST.get("resultdict[FPassage]", '')

    Pedpassage_info =  T_PedPassage.objects.filter(Q(FPassage__contains=serinput), Q(CREATED_PRJ=prjid))
    Pedpassage_info = org_split(Pedpassage_info, request)

    dict = convert_to_dicts(Pedpassage_info)
    resultdict = {'code':0, 'msg':"", 'count': Pedpassage_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    prjid = request.session['PrjID']

    device_info = device.objects.filter(Q(FStatus=True))
    area_info = area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prjid))

    obj.fields['FDevID'].choices = get_dict_object(request, device_info, 'FID', 'FDevice')
    obj.fields['FAreaID'].choices = get_dict_object(request, area_info, 'FID', 'FName')

#链接增加模板
def add(request):
    obj = PedPassageModelForm()

    ref_dropdowndata(obj, request)
    return render(request, "content/pedpassage/pedpassageadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Pedpassage_info = T_PedPassage.objects.get(Q(FID=fid))
    obj = PedPassageModelForm(instance=Pedpassage_info)

    ref_dropdowndata(obj, request)

    return render(request, "content/pedpassage/pedpassageadd.html", {'obj': obj, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = PedPassageModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Pedpassage_info = T_PedPassage.objects.get(FID=fid)
            obj = PedPassageModelForm(request.POST, instance=Pedpassage_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        ref_dropdowndata(obj, request)

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                if request.GET.get('actype') == 'insert':
                    temp.FStatus = True
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

#处理禁用/启用班组
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Pedpassage_info = T_PedPassage.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Pedpassage_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Pedpassage_info.FStatus = True

            Pedpassage_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))





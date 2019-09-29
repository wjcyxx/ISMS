from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import device as T_Device
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
def device(request):
    devicetype_info = base.objects.filter(Q(FPID='8feb17b2aaf211e99741708bcdb9b39a'))
    devicetypeinfo = get_dict_table(devicetype_info, 'FID', 'FBase')

    return render(request, 'content/device/deviceinfo.html', {'devicetypeinfo': devicetypeinfo})


#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FDevice]", '')

    Device_info =  T_Device.objects.filter(Q(FDevice__contains=serinput))

    dict = convert_to_dicts(Device_info)
    resultdict = {'code':0, 'msg':"", 'count': Device_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    devicetype_info = base.objects.filter(Q(FPID='8feb17b2aaf211e99741708bcdb9b39a'))
    interpos_info = base.objects.filter(Q(FPID__isnull=True))

    obj.fields['FDevtypeID'].choices = get_dict_object(request, devicetype_info, 'FID', 'FBase')
    obj.fields['FInterfacePos'].choices = get_dict_object(request, interpos_info, 'FID', 'FBase')

#链接增加模板
def add(request):
    if request.method == 'GET':

        obj = DeviceModelForm()
        ref_dropdowndata(obj, request)
        return render(request, "content/device/deviceadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Device_info = T_Device.objects.get(Q(FID=fid))
    obj = DeviceModelForm(instance=Device_info)

    ref_dropdowndata(obj, request)

    return render(request, "content/device/deviceadd.html", {'obj': obj, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = DeviceModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Device_info = T_Device.objects.get(FID=fid)
            obj = DeviceModelForm(request.POST, instance=Device_info)
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
            Device_info = T_Device.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Device_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Device_info.FStatus = True

            Device_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))





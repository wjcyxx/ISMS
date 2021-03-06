from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import devinterface as T_DevInterface
from .models import subinterface as T_SubInterface
from .models import interfaceparam as T_InterfaceParam
from device.models import device
from appkey.models import appkey
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from django.conf import settings
import os
from threading import Thread
import inspect
import ctypes

# Create your views here.
#接口管理控制器入口
def devinterface(request):
    device_info = device.objects.filter(Q(FStatus=True))
    deviceinfo = get_dict_table(device_info, 'FID', 'FDevice')

    interfacetype_info = base.objects.filter(Q(FPID='08a3e2b0ab7a11e9891f708bcdb9b39a'))
    interfacetypeinfo = get_dict_table(interfacetype_info, 'FID', 'FBase')

    return render(request, 'content/devinterface/devinterfaceinfo.html', {'deviceinfo': deviceinfo, 'interfacetypeinfo': interfacetypeinfo})


#返回table数据及查询结果
def get_datasource(request):
    prj_id = request.session['PrjID']
    serinput = request.POST.get("resultdict[FName]", '')
    org_id = prj_2_manageorg(prj_id)

    Devinterface_info =  T_DevInterface.objects.filter(Q(FName__contains=serinput), Q(CREATED_PRJ=prj_id) | Q(CREATED_ORG=org_id) | Q(FScope=2))
    #Devinterface_info = org_split(Devinterface_info, request)

    dict = convert_to_dicts(Devinterface_info)
    resultdict = {'code':0, 'msg':"", 'count': Devinterface_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#返回子接口数据
class get_subinterface_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        fid  = ''.join(str(self.request.GET.get('fpid')).split('-'))
        serinput = self.request.POST.get("resultdict[FInterfaceID]", '')

        subinterface_info = T_SubInterface.objects.filter(Q(FPID=fid), FInterfaceID__contains=serinput)
        return subinterface_info


#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    device_info = device.objects.filter(Q(FStatus=True))
    interfacetype_info = base.objects.filter(Q(FPID='08a3e2b0ab7a11e9891f708bcdb9b39a'))
    interext_info = base.objects.filter(Q(FPID__isnull=False)).order_by('FBaseID')
    appkey_info = appkey.objects.filter(Q(FStatus=True), Q(FType=1))

    obj.fields['FDevID'].choices = get_dict_object(request, device_info, 'FID', 'FDevice')
    obj.fields['FInterfaceTypeID'].choices = get_dict_object(request, interfacetype_info, 'FID', 'FBase')
    obj.fields['FInterfaceExtID'].choices = get_dict_object(request, interext_info, 'FID', 'FBase')
    obj.fields['FAppFID'].choices = get_dict_object(request, appkey_info, 'FID', 'FAppName')

#链接增加模板
def add(request):
    obj = DeviceInterfaceModelForm()

    ref_dropdowndata(obj, request)
    return render(request, "content/devinterface/devinterfaceadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Devinterface_info = T_DevInterface.objects.get(Q(FID=fid))
    obj = DeviceInterfaceModelForm(instance=Devinterface_info)
    ref_dropdowndata(obj, request)

    paramtype_info = base.objects.filter(Q(FPID='8ad84c1aabb811e996a1708bcdb9b39a'))
    paramtypeinfo = get_dict_table(paramtype_info, 'FID', 'FBase')

    subinterface_info = T_DevInterface.objects.filter(Q(FInterfaceAttribID=0))
    subinterfaceinfo = get_dict_table(subinterface_info, 'FID', 'FName')

    return render(request, "content/devinterface/devinterfaceadd.html", {'obj': obj, 'devintrerface': Devinterface_info, 'paramtypeinfo': paramtypeinfo, 'subinterfaceinfo': subinterfaceinfo, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = DeviceInterfaceModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Devinterface_info = T_DevInterface.objects.get(FID=fid)
            obj = DeviceInterfaceModelForm(request.POST, instance=Devinterface_info)
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

#处理禁用/启用参数
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Devinterface_info = T_DevInterface.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Devinterface_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Devinterface_info.FStatus = True

            Devinterface_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))


#处理删除服务组内子接口
class del_subint(delete_base):
    def set_view(self,request):
        self.response_data['result'] = '0'
        self.model = T_SubInterface


#处理刷新下拉列表数据源
def ref_paramdropdown(obj, request):
    type_info = base.objects.filter(Q(FPID='8ad84c1aabb811e996a1708bcdb9b39a'))

    obj.fields['FTypeID'].choices = get_dict_object(request, type_info, 'FID', 'FBase')


#链接增加参数view
def addparam(request):

    if request.method == 'GET':
        fpid = ''.join(str(request.GET.get('fid')).split('-'))

        obj = InterfaceParamModelForm()
        ref_paramdropdown(obj, request)

        devinterface_info = T_DevInterface.objects.get(Q(FID=fpid))
        DeviceInterfaceForm = DeviceInterfaceModelForm(instance=devinterface_info)
        ref_dropdowndata(DeviceInterfaceForm, request)

        return render(request, "content/devinterface/interfaceparamadd.html" , {'obj': obj, 'DeviceInterfaceForm': DeviceInterfaceForm, 'fpid': fpid, 'action': 'insert'})

#链接编辑参数view
def editparam(request):
    if request.method == 'GET':
        fpid = ''.join(str(request.GET.get('fpid')).split('-'))
        fid = ''.join(str(request.GET.get('fid')).split('-'))

        param_info = T_InterfaceParam.objects.get(Q(FID=fid))
        obj = InterfaceParamModelForm(instance=param_info)
        ref_paramdropdown(obj, request)

        devinterface_info = T_DevInterface.objects.get(Q(FID=fpid))
        DeviceInterfaceForm = DeviceInterfaceModelForm(instance=devinterface_info)
        ref_dropdowndata(DeviceInterfaceForm, request)

        return render(request, "content/devinterface/interfaceparamadd.html" , {'obj': obj, 'DeviceInterfaceForm': DeviceInterfaceForm, 'fpid': fpid, 'action': 'update'})

#处理插入参数
def param_insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = InterfaceParamModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            InterfaceParam_info = T_InterfaceParam.objects.get(FID=fid)
            obj = InterfaceParamModelForm(request.POST, instance=InterfaceParam_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        ref_paramdropdown(obj, request)

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                temp.FPID = request.GET.get('fpid')
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


#返回参数table数据源
def get_paramdatasource(request):
    serinput = request.POST.get("resultdict[FParam]", '')
    fpid = ''.join(str(request.GET.get('fpid')).split('-'))

    InterfaceParam_info =  T_InterfaceParam.objects.filter(Q(FPID=fpid), Q(FParam__contains=serinput)).order_by('FSequence')

    dict = convert_to_dicts(InterfaceParam_info)
    resultdict = {'code':0, 'msg':"", 'count': InterfaceParam_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#处理删除参数
def param_delete(request):
    if request.method == 'POST':

        response_data = {}
        fid = request.POST.get('currfid')

        try:
            T_InterfaceParam.objects.get(FID=fid).delete()
            response_data['result'] = '0'
        except:
            response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))



class subinterface_add(add_base):
    def set_view(self, request):
        self.template_name = 'content/devinterface/subinterfaceadd.html'

        self.objForm = SubInterfaceModelForm
        self.query_sets = [
            T_DevInterface.objects.filter(Q(FStatus=True), Q(FInterfaceAttribID=0))
        ]
        self.query_set_idfields = ['FInterfaceID']
        self.query_set_valuefields = ['FName']
        self.context['fid'] = ''.join(str(self.request.GET.get('fid')).split('-'))


class subinterface_insert(insert_base):
    def set_view(self, request):
        self.model = T_SubInterface
        self.type = 1
        self.objForm = SubInterfaceModelForm

        self.query_sets = [
            T_DevInterface.objects.filter(Q(FStatus=True), Q(FInterfaceAttribID=0))
        ]
        self.query_set_idfields = ['FInterfaceID']
        self.query_set_valuefields = ['FName']








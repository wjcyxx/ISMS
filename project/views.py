from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from basedata.models import base
from organize.models import organize as T_Organize
from django.db.models import Q
from common.views import *
from .models import project as T_Project
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist

#项目管理控制器入口
def project(request):
    #传递工程类别字典到前台页面
    prjtype_info = base.objects.filter(Q(FPID='4a94b19ea3d811e9b984708bcdb9b39a'))
    prjtype = get_dict_table(prjtype_info, 'FID', 'FBase')

    #传递工程用途字典到前台页面
    prjuse_info = base.objects.filter(Q(FPID='71921f42a3d911e9920c708bcdb9b39a'))
    prjuse = get_dict_table(prjuse_info, 'FID', 'FBase')

    #传递工程状态字典到前台页面
    prjstate_info = base.objects.filter(Q(FPID='22682ae6a3da11e9920c708bcdb9b39a'))
    prjstate = get_dict_table(prjstate_info, 'FID', 'FBase')

    #传递结构类型字典到前台页面
    prjstruc_info = base.objects.filter(Q(FPID='97cfc154a3da11e9920c708bcdb9b39a'))
    prjstruc = get_dict_table(prjstruc_info, 'FID', 'FBase')

    #传递管理组织字典到前台页面
    prjmanorg_info = T_Organize.objects.filter(Q(FStatus=True))
    prjmanorg = get_dict_table(prjmanorg_info, 'FID', 'FOrgname')

    #传递所有变量至前台模板
    return render(request, 'content/project/projectinfo.html', locals())

#返回table数据及查询结果
def get_datasource(request):
    Orgid = request.session['UserOrg']

    serinput = request.POST.get("resultdict[FPrjname]", '')
    condtions = {"FManageORG": Orgid}

    Project_info =  T_Project.objects.filter(Q(FPrjname__contains=serinput))
    Project_info = org_split(Project_info, request, **condtions)

    dict = convert_to_dicts(Project_info)
    resultdict = {'code':0, 'msg':"", 'count': Project_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    prjtype_info = base.objects.filter(Q(FPID='4a94b19ea3d811e9b984708bcdb9b39a'))
    prjuse_info = base.objects.filter(Q(FPID='71921f42a3d911e9920c708bcdb9b39a'))
    prjstate_info = base.objects.filter(Q(FPID='22682ae6a3da11e9920c708bcdb9b39a'))
    prjstruc_info = base.objects.filter(Q(FPID='97cfc154a3da11e9920c708bcdb9b39a'))
    prjmanorg_info = T_Organize.objects.filter(Q(FStatus=True))

    obj.fields['FPrjtypeID'].choices = get_dict_object(request, prjtype_info, 'FID', 'FBase')
    obj.fields['FPrjuseID'].choices = get_dict_object(request, prjuse_info, 'FID', 'FBase')
    obj.fields['FPrjstate'].choices = get_dict_object(request, prjstate_info, 'FID', 'FBase')
    obj.fields['FStructypeID'].choices = get_dict_object(request, prjstruc_info, 'FID', 'FBase')
    obj.fields['FManageORG'].choices = get_dict_object(request, prjmanorg_info, 'FID', 'FOrgname')


#链接增加模板
def add(request):
    type = request.GET.get('type')
    obj = ProjectModelForm()

    ref_dropdowndata(obj, request)
    return render(request, "content/project/projectadd.html" , {'obj': obj, 'action': 'insert', 'type': type})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Project_info = T_Project.objects.get(Q(FID=fid))
    obj = ProjectModelForm(instance=Project_info)

    ref_dropdowndata(obj, request)
    return render(request, "content/project/projectadd.html", {'obj': obj,  'Project_info': Project_info,  'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = ProjectModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Project_info = T_Project.objects.get(FID=fid)
            obj = ProjectModelForm(request.POST, instance=Project_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        ref_dropdowndata(obj, request)

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                temp.FStatus = True
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

#处理禁用/启用项目
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Project_info = T_Project.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Project_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Project_info.FStatus = True

            Project_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))

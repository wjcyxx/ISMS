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
    prjmanorg = get_dict_table(prjmanorg_info, 'FID', 'FBase')

    #传递所有变量至前台模板
    return render(request, 'content/project/projectinfo.html', locals())

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FPrjname]", '')

    Project_info =  T_Project.objects.filter(Q(FPrjname__contains=serinput))

    dict = convert_to_dicts(Project_info)
    resultdict = {'code':0, 'msg':"", 'count': Project_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#链接增加模板
def add(request):
    obj = ProjectModelForm()

    prjtype_info = base.objects.filter(Q(FPID='4a94b19ea3d811e9b984708bcdb9b39a'))
    obj.fields['FPrjtypeID'].choices = get_dict_object(request, prjtype_info, 'FID', 'FBase')

    prjuse_info = base.objects.filter(Q(FPID='71921f42a3d911e9920c708bcdb9b39a'))
    obj.fields['FPrjtypeID'].choices = get_dict_object(request, prjuse_info, 'FID', 'FBase')


    return render(request, "content/project/projectadd.html" , {'obj': obj, 'action': 'insert'})


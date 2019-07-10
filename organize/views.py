from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import organize as T_Organize
from basedata.models import base
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist

#User管理控制器入口
def organize(request):
    #传递组织类型字典到前台页面
    setdata_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
    setdata = get_dict_table(setdata_info, 'FID', 'FBase')

    return render(request, 'content/organize/organizeinfo.html', {'setdata': setdata})

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FOrgname]", '')

    Organize_info = T_Organize.objects.filter(Q(FOrgname__contains=serinput))

    dict = convert_to_dicts(Organize_info)
    resultdict = {'code':0, 'msg':"", 'count': Organize_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#链接增加模板
def add(request):
    obj = OrganizeModelForm()

    Orgtype_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
    obj.fields['FOrgtypeID'].choices = get_dict_object(request, Orgtype_info, 'FID', 'FBase')

    return render(request, "content/organize/organizeadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Organize_info = T_Organize.objects.get(FID=fid)
    obj = OrganizeModelForm(instance=Organize_info)

    Orgtype_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
    obj.fields['FOrgtypeID'].choices = get_dict_object(request, Orgtype_info, 'FID', 'FBase')

    return render(request, "content/organize/organizeadd.html", {'obj': obj, 'Organize_info': Organize_info, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = OrganizeModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Orgtype_info = T_Organize.objects.get(FID=fid)
            obj = OrganizeModelForm(request.POST, instance=Orgtype_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))


        Orgtype_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
        obj.fields['FOrgtypeID'].choices = get_dict_object(request, Orgtype_info, 'FID', 'FBase')

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                temp.FIssplit = True
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


#处理禁用设备
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Orgtype_info = T_Organize.objects.get(FID=fid)

            Orgtype_info.FStatus = False
            Orgtype_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))




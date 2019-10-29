from django.shortcuts import render
from django.shortcuts import HttpResponse
from login.models import *
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
from organize.models import organize
from usergroup.models import usergroup
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist

#User管理控制器入口
def user(request):
    return render(request, 'content/user/userinfo.html')

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FBase]", '')
    Orgid = request.session['UserOrg']

    User_info = User.objects.filter(Q(FUserID__contains=serinput))
    condtions = {"FOrgID": Orgid}
    User_info = org_split(User_info, request, **condtions)

    dict = convert_to_dicts(User_info)
    resultdict = {'code':0, 'msg':"", 'count': User_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)


def ref_dropdowndata(obj, request):
    Organize_info = organize.objects.filter(Q(FStatus=True))
    Usergroup_info = usergroup.objects.filter(Q(FStatus=True))

    obj.fields['FOrgID'].choices = get_dict_object(request, Organize_info, 'FID', 'FOrgname')
    obj.fields['FRoleID'].choices = get_dict_object(request, Usergroup_info, 'FID', 'FName')

#链接增加模板
def add(request):
    obj = UserModelForm()

    ref_dropdowndata(obj, request)
    return render(request, "content/user/useradd.html" , {'obj': obj, 'action': 'insert'})


#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    User_info = User.objects.get(FID=fid)
    obj = UserModelForm(instance=User_info)

    ref_dropdowndata(obj, request)
    return render(request, "content/user/useradd.html", {'obj': obj, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = UserModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            User_info = User.objects.get(FID=fid)
            obj = UserModelForm(request.POST, instance=User_info)
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


#处理禁用用户
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            User_info = User.objects.get(FID=fid)

            User_info.FStatus = False
            User_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))




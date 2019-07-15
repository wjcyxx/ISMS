from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import team as T_Team
from organize.models import organize
from group.models import group
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

#施工队管理控制器入口
def team(request):
    org_info = organize.objects.filter(Q(FStatus=True))
    orginfo = get_dict_table(org_info, 'FID', 'FOrgname')

    return render(request, 'content/team/teaminfo.html', {'orginfo': orginfo})


#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FName]", '')

    prj_id = request.session['PrjID']

    Team_info =  T_Team.objects.filter(Q(FName__contains=serinput), Q(CREATED_PRJ=prj_id))

    dict = convert_to_dicts(Team_info)
    resultdict = {'code':0, 'msg':"", 'count': Team_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#返回班组数据列表
def get_workdatasource(request):

    fid = request.GET.get('fid')
    group_info = group.objects.filter(Q(FTeamID=fid))

    dict = convert_to_dicts(group_info)
    resultdict = {'code':0, 'msg':"", 'count': group_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)


#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    org_info = organize.objects.filter(Q(FStatus=True))

    obj.fields['FOrgID'].choices = get_dict_object(request, org_info, 'FID', 'FOrgname')


#链接增加模板
def add(request):
    obj = TeamModelForm()

    ref_dropdowndata(obj, request)
    return render(request, "content/team/teamadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Team_info = T_Team.objects.get(Q(FID=fid))
    obj = TeamModelForm(instance=Team_info)

    ref_dropdowndata(obj, request)

    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
    worktypeinfo = get_dict_table(worktype_info, 'FID', 'FBase')


    return render(request, "content/team/teamadd.html", {'obj': obj, 'worktypeinfo': worktypeinfo, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = TeamModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Team_info = T_Team.objects.get(FID=fid)
            obj = TeamModelForm(request.POST, instance=Team_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        ref_dropdowndata(obj, request)

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                if request.GET.get('actype') == 'insert':
                    temp.FStatus = True
                    temp.FEvaluate = 0
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

#处理禁用/启用施工队
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Team_info = T_Team.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Team_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Team_info.FStatus = True

            Team_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))




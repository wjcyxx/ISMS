from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import group as T_Group
from team.models import team
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
from team.forms import TeamModelForm
from organize.models import organize
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
#班组管理控制器入口
def group(request):
    prj_id = request.session['PrjID']

    team_info = team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
    teaminfo = get_dict_table(team_info, 'FID', 'FName')

    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
    worktypeinfo = get_dict_table(worktype_info, 'FID', 'FBase')

    return render(request, 'content/group/groupinfo.html', {'teaminfo': teaminfo, 'worktypeinfo': worktypeinfo})


#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FGroup]", '')

    prj_id = request.session['PrjID']

    Group_info =  T_Group.objects.filter(Q(FGroup__contains=serinput), Q(CREATED_PRJ=prj_id))

    dict = convert_to_dicts(Group_info)
    resultdict = {'code':0, 'msg':"", 'count': Group_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    team_info = team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=request.session['PrjID']))
    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))

    obj.fields['FTeamID'].choices = get_dict_object(request, team_info, 'FID', 'FName')
    obj.fields['FWorktypeID'].choices = get_dict_object(request, worktype_info, 'FID', 'FBase')

#链接增加模板
def add(request):
    if request.method == 'GET':
        fteamid = ''.join(str(request.GET.get('fid')).split('-'))

        obj = GroupModelForm()

        team_info = team.objects.get(Q(FID=fteamid))
        TeamForm = TeamModelForm(instance=team_info)

        org_info = organize.objects.filter(Q(FStatus=True))
        TeamForm.fields['FOrgID'].choices = get_dict_object(request, org_info, 'FID', 'FOrgname')

        ref_dropdowndata(obj, request)
        return render(request, "content/group/groupadd.html" , {'obj': obj, 'TeamForm': TeamForm, 'fteamid': fteamid, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Group_info = T_Group.objects.get(Q(FID=fid))
    fteamid = Group_info.FTeamID
    obj = GroupModelForm(instance=Group_info)

    team_info = team.objects.get(Q(FID=fteamid))
    TeamForm = TeamModelForm(instance=team_info)

    ref_dropdowndata(obj, request)

    return render(request, "content/group/groupadd.html", {'obj': obj, 'fteamid': fteamid, 'TeamForm': TeamForm, 'action': 'update'})

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        fteamid = request.GET.get('fteamid')

        if request.GET.get('actype') == 'insert':
            obj = GroupModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Group_info = T_Group.objects.get(FID=fid)
            obj = GroupModelForm(request.POST, instance=Group_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        ref_dropdowndata(obj, request)

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                if request.GET.get('actype') == 'insert':
                    temp.FStatus = True
                temp.FTeamID = fteamid
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
            Group_info = T_Group.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Group_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Group_info.FStatus = True

            Group_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))





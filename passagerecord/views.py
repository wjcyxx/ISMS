from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from pedpassage.models import passagerecord as T_PassageRecord
from personnel.models import personnel
from pedpassage.models import pedpassage
from area.models import area
from group.models import group
from basedata.models import base
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

# Create your views here.
#通道记录(考勤查询)控制器入口
def passagerecord(request):
    prj_id = request.session['PrjID']

    authtype_info = base.objects.filter(Q(FPID='2cd8b28cacf111e991437831c1d24216'))
    authtypeinfo = get_dict_table(authtype_info, 'FID', 'FBase')

    area_info = area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
    areainfo = get_dict_table(area_info, 'FID', 'FName')

    group_info = group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
    groupinfo = get_dict_table(group_info, 'FID', 'FGroup')

    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
    worktypeinfo = get_dict_table(worktype_info, 'FID', 'FBase')

    return render(request, 'content/passagerecord/passagerecordinfo.html', locals())

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FPersonID__FName]", '')

    prj_id = request.session['PrjID']

    passagerecord_info =  T_PassageRecord.objects.filter(Q(FPersonID__FName__contains=serinput), Q(CREATED_PRJ=prj_id)).values('FPersonID__FName','FPersonID__FGroupID', 'FPersonID__FWorktypeID', 'FPassageID__FAreaID', 'FPassageID__FPassage', 'FPassageID__FType', 'FAuthtypeID', 'CREATED_TIME' )

    dict = list(passagerecord_info)
    resultdict = {'code':0, 'msg':"", 'count': passagerecord_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

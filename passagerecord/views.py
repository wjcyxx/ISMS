from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from pedpassage.models import passagerecord as T_PassageRecord
from personnel.models import personnel
from pedpassage.models import pedpassage
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

    person_info = personnel.objects.filter(Q(FStatus=0), Q(CREATED_PRJ=prj_id))
    personinfo = get_dict_table(person_info, 'FID', 'FName')

    passage_info = pedpassage.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
    passageinfo = get_dict_table(passage_info, 'FID', 'FPassage')

    authtype_info = base.objects.filter(Q(FPID='2cd8b28cacf111e991437831c1d24216'))
    authtypeinfo = get_dict_table(authtype_info, 'FID', 'FBase')

    return render(request, 'content/passagerecord/passagerecordinfo.html', locals())

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FName]", '')

    prj_id = request.session['PrjID']

    passagerecord_info =  T_PassageRecord.objects.filter(Q(FPersonID__FName__contains=serinput), Q(CREATED_PRJ=prj_id)).values('FPersonID__FName','FPersonID__FWorktypeID')

    #passagerecord_info =  T_PassageRecord.objects.filter(Q(FPersonID__FName__contains=serinput), Q(CREATED_PRJ=prj_id))

    dict = list(passagerecord_info)

    #dict = convert_to_dicts(passagerecord_info))
    resultdict = {'code':0, 'msg':"", 'count': passagerecord_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

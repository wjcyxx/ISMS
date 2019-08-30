from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from team.models import team
from personnel.models import personnel
from pedpassage.models import passagerecord
from pedpassage.models import pedpassage
from personauth.models import personauth
from group.models import group
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
from django.db import connection
from django.db.models import Sum, Count


class topanalyse(View):
    def post(self, request):
        prj_id = request.session['PrjID']

        team_info = team.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=True))

        group_info = group.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=True))

        #员工登记，退场，禁用数量
        dengji_info = personnel.objects.filter(~Q(FType=0), Q(FStatus=0))
        tuichang_info = personnel.objects.filter(~Q(FType=0),Q(FStatus=1))
        jinyong_info = personnel.objects.filter(~Q(FType=0),Q(FStatus=2))

        #人行通道统计信息
        pedpassage_info = pedpassage.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=True))

        zsauth_info = personauth.objects.filter(Q(CREATED_PRJ=prj_id), Q(FAuthtype=0)).values('FPersonID').annotate(auth_sum=Count('FPersonID'))

        # zsauth_count = 0
        # for j in zsauth_info:
        #     zsauth_count = zsauth_count + j['auth_sum'] if (len(zsauth_info)!=0) else 0

        response_data = {}
        response_data['team_count'] = team_info.count()
        response_data['group_count'] = group_info.count()
        response_data['dengji_count'] = dengji_info.count()
        response_data['tuichang_count'] = tuichang_info.count()
        response_data['jinyong_count'] = jinyong_info.count()
        response_data['teamhg_count'] = team_info.filter(Q(FEvaluate=0)).count()
        response_data['teambhg_count'] = team_info.filter(Q(FEvaluate=1)).count()
        response_data['pedpassage_count'] = pedpassage_info.count()
        response_data['zsauth_count'] = len(zsauth_info)

        return HttpResponse(json.dumps(response_data))



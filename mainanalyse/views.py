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
from vehiclegate.models import vehiclegate
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
        lsauth_info = personauth.objects.filter(Q(CREATED_PRJ=prj_id), Q(FAuthtype=1)).values('FPersonID').annotate(auth_sum=Count('FPersonID'))

        #车行通道统计信息
        vehgate_info = vehiclegate.objects.filter(Q(CREATED_PRJ=prj_id), Q(FStatus=True))

        response_data = {}
        response_data['team_count'] = team_info.count()
        response_data['group_count'] = group_info.count()
        response_data['dengji_count'] = dengji_info.count()
        response_data['tuichang_count'] = tuichang_info.count()
        response_data['jinyong_count'] = jinyong_info.count()
        response_data['teamhg_count'] = team_info.filter(Q(FEvaluate=0)).count()
        response_data['teambhg_count'] = team_info.filter(Q(FEvaluate=1)).count()
        response_data['pedpassage_count'] = pedpassage_info.count()
        response_data['pedrk_count'] = pedpassage_info.filter(Q(FType=0)).count()
        response_data['pedck_count'] = pedpassage_info.filter(Q(FType=1)).count()
        response_data['zsauth_count'] = len(zsauth_info)
        response_data['lsauth_count'] = len(lsauth_info)
        response_data['vehgate_count'] = vehgate_info.count()
        response_data['vehgaterk_count'] = vehgate_info.filter(Q(FGatetype=0)).count()
        response_data['vehgateck_count'] = vehgate_info.filter(Q(FGatetype=1)).count()

        return HttpResponse(json.dumps(response_data))

class pedpassageanlayse(View):
    def post(self, request):
        end_time = datetime.datetime.now()
        begin_time = (end_time - datetime.timedelta(days=6))

        end_time = end_time.strftime('%Y-%m-%d')
        begin_time = begin_time.strftime('%Y-%m-%d')

        cur = connection.cursor()

        sqlstr = "SELECT DATE_FORMAT(dday,'%m-%d') AS dt1,count(*)-1 AS FCust FROM (SELECT datelist AS dday FROM calendar WHERE datelist BETWEEN '"+ begin_time +"' AND '"+ end_time +"' UNION ALL SELECT DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') AS dt FROM T_PassageRecord AS a LEFT JOIN T_PedPassage AS b ON a.FPassageID_id=b.FID WHERE b.FStatus=1 AND b.FType=0 AND DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') BETWEEN '"+ begin_time +"' AND '"+ end_time +"') a GROUP BY dt1"

        cur.execute(sqlstr)
        rows = cur.fetchall()

        response_days = []
        response_rk_value = []
        response_ck_value = []

        for r in rows:
            response_days.append(r[0])
            response_rk_value.append(r[1])


        cur1 = connection.cursor()

        sqlstr = "SELECT DATE_FORMAT(dday,'%m-%d') AS dt1,count(*)-1 AS FCust FROM (SELECT datelist AS dday FROM calendar WHERE datelist BETWEEN '"+ begin_time +"' AND '"+ end_time +"' UNION ALL SELECT DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') AS dt FROM T_PassageRecord AS a LEFT JOIN T_PedPassage AS b ON a.FPassageID_id=b.FID WHERE b.FStatus=1 AND b.FType=1 AND DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') BETWEEN '"+ begin_time +"' AND '"+ end_time +"') a GROUP BY dt1"


        cur1.execute(sqlstr)
        rows1 = cur1.fetchall()

        for r1 in rows1:
            response_ck_value.append([r1[1]])

        result_dict = {'FDay': response_days, 'FRkvalue': response_rk_value, 'FCkvalue': response_ck_value}

        return JsonResponse(result_dict, safe=False)

from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from team.models import team
from pedpassage.models import passagerecord
from personnel.models import personnel
from pedpassage.models import pedpassage
from vehiclegate.models import vehiclegate
from vehiclepasslog.models import vehiclepasslog
from personauth.models import personauth
from group.models import group
from basedata.models import base
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
from django.db import connection
from django.db.models import Sum, Count
import re

#顶部统计瓷砖数据
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


#人行通道吞吐量分析数据
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
            response_ck_value.append(r1[1])

        result_dict = {'FDay': response_days, 'FRkvalue': response_rk_value, 'FCkvalue': response_ck_value}

        return JsonResponse(result_dict, safe=False)


#车行通道吞吐量数据分析
class vehpassageanalyse(View):
    def post(self, request):
        end_time = datetime.datetime.now()
        begin_time = (end_time - datetime.timedelta(days=6))

        end_time = end_time.strftime('%Y-%m-%d')
        begin_time = begin_time.strftime('%Y-%m-%d')

        cur = connection.cursor()

        sqlstr = "SELECT DATE_FORMAT(dday,'%m-%d') AS dt1,count(*)-1 AS FCust FROM (SELECT datelist AS dday FROM calendar WHERE datelist BETWEEN '"+ begin_time +"' AND '"+ end_time +"' UNION ALL SELECT DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') AS dt FROM T_VehiclePassLog AS a LEFT JOIN T_VehicleGate AS b ON a.FGateID_id=b.FID WHERE b.FStatus=1 AND b.FGatetype=0 AND DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') BETWEEN '"+ begin_time +"' AND '"+ end_time +"') a GROUP BY dt1"

        cur.execute(sqlstr)
        rows = cur.fetchall()

        response_days = []
        response_rk_value = []
        response_ck_value = []

        for r in rows:
            response_days.append(r[0])
            response_rk_value.append(r[1])

        cur1 = connection.cursor()

        sqlstr = "SELECT DATE_FORMAT(dday,'%m-%d') AS dt1,count(*)-1 AS FCust FROM (SELECT datelist AS dday FROM calendar WHERE datelist BETWEEN '"+ begin_time +"' AND '"+ end_time +"' UNION ALL SELECT DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') AS dt FROM T_VehiclePassLog AS a LEFT JOIN T_VehicleGate AS b ON a.FGateID_id=b.FID WHERE b.FStatus=1 AND b.FGatetype=1 AND DATE_FORMAT(a.CREATED_TIME,'%Y-%m-%d') BETWEEN '"+ begin_time +"' AND '"+ end_time +"') a GROUP BY dt1"


        cur1.execute(sqlstr)
        rows1 = cur1.fetchall()

        for r1 in rows1:
            response_ck_value.append(r1[1])

        result_dict = {'FDay': response_days, 'FRkvalue': response_rk_value, 'FCkvalue': response_ck_value}

        return JsonResponse(result_dict, safe=False)


#人行最新通行动态数据
class get_pedpassage_news(View):
    def post(self, request):
        prj_id = request.session['PrjID']

        passagerecord_info = passagerecord.objects.filter(Q(CREATED_PRJ=prj_id)).values('FID','FPersonID__FName', 'FPersonID__FGroupID', 'FPersonID__FPhoto', 'FPassageID__FPassage', 'FPassageID__FType', 'FAuthtypeID', 'CREATED_TIME').order_by('-CREATED_TIME')

        result_dict = []

        for dt in list(passagerecord_info):
            dict = {}

            dict['FID'] = ''.join(str(dt['FID']).split('-'))
            dict['FPersonName'] = dt['FPersonID__FName']
            dict['CREATED_TIME'] = timezone.datetime.strftime(dt['CREATED_TIME'], '%Y-%m-%d %H:%M:%S')

            group_id = dt['FPersonID__FGroupID']
            dict['FGroup'] = group.objects.get(Q(FID=group_id)).FGroup
            dict['FPhoto'] = dt['FPersonID__FPhoto']
            dict['FPassage'] = dt['FPassageID__FPassage']
            authtype_id = dt['FAuthtypeID']
            dict['FAuthtype'] = base.objects.get(Q(FID=authtype_id)).FBase
            if dt['FPassageID__FType'] == 0:
                dict['FPassageType'] = '入口'
            else:
                dict['FPassageType'] = '出口'

            result_dict.append(dict)

        return HttpResponse(json.dumps(result_dict))


#车行最新通行动态数据
class get_vehpassage_news(View):
    def post(self, request):
        prj_id = request.session['PrjID']

        vehpasslog_info = vehiclepasslog.objects.filter(Q(CREATED_PRJ=prj_id)).values('FID', 'FPlate', 'FGateID__FGate', 'CREATED_TIME', 'FGateID__FGatetype', 'FGateID__FGateattr', 'FPlate__FVehicletypeID')

        result_dict = []

        for dt in list(vehpasslog_info):
            dict = {}

            dict['FID'] = ''.join(str(dt['FID']).split('-'))
            dict['FPlate'] = dt['FPlate']
            dict['FGate'] = dt['FGateID__FGate']
            dict['CREATED_TIME'] = timezone.datetime.strftime(dt['CREATED_TIME'], '%Y-%m-%d %H:%M:%S')
            if dt['FGateID__FGatetype'] == 0:
                dict['FGateType'] = '入口'
            else:
                dict['FGateType'] = '出口'

            dict['FGateAttrID'] = dt['FGateID__FGateattr']

            if dt['FGateID__FGateattr'] == 0:
                dict['FGateAttr'] = '普通通道'
            else:
                dict['FPassageType'] = '货运通道'

            vehicletype_id = dt['FPlate__FVehicletypeID']
            dict['FVehicletype'] = base.objects.get(Q(FID=vehicletype_id)).FBase
            dict['FPhoto'] = base.objects.get(Q(FID=vehicletype_id)).FDesc

            result_dict.append(dict)

        return HttpResponse(json.dumps(result_dict))



class envanalyse(View):
    def post(self, request):
        devkey = request.POST.get('Deykey')
        devdate = str(request.POST.get('Devdate')).split(' - ')
        devdate[0] = devdate[0].replace('-', '') + '0000'
        devdate[1] = devdate[1].replace('-', '') + '2359'


        params = [devkey, devdate[0], devdate[1]]

        initID = '36f221ccc53d11e98ea67831c1d24216'
        url = get_interface_url(initID)
        s = get_interface_param(initID)

        param = urllib.parse.unquote(s)
        key = re.findall(r"\$\{.*?\}", param)

        for i in range(len(key)):
            param = param.replace(key[i], params[i])

        req = url + '?' + param

        response = urllib.request.urlopen(req)
        data = response.read()
        data = data.decode('utf-8')

        result = json.loads(data)

        result = result['HisData']

        TimeValues = []
        TempValues = []
        HumiValues = []

        for r in result:
            TimeValues.append(r['TimeValue'])
            TempValues.append(r['TempValue'])
            HumiValues.append(r['HumiValue'])


        result_dict = {'TimeValues': TimeValues, 'TempValues': TempValues, 'HumiValues': HumiValues}

        return JsonResponse(result_dict, safe=False)










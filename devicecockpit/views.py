from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q, Sum, Count
from basedata.models import base
from project.models import project
from device.models import device
from devinterfacesrv.models import envinterfacesrv
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
from django.db import connection

# Create your views here.

#万物互联环境监测
class envcockpit_entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/datacockpit/devcockpit.html'

        device_info = device.objects.filter(Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a'))

        self.context['envdev_count'] = device_info.count()
        self.context['enable_count'] = device_info.filter(Q(FStatus=True))
        self.context['disable_count'] = device_info.filter(Q(FStatus=False))


class get_envrealtimedata(View):
    def post(self, request):
        prjID = ''.join(str(request.POST.get('prjid')).split('-'))

        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        begin_time = (datetime.datetime.now() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")

        if prjID == '':
            #device_info = device.objects.filter(Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a')).first()
            cur = connection.cursor()

            sqlstr = "SELECT FORMAT(AVG(FPM25),1) as FPM25, FORMAT(AVG(FPM10), 1) as FPM10, FORMAT(AVG(FSPM), 1) as FSPM, FORMAT(AVG(FWIND_SPEED), 1) as FWIND_SPEED, FORMAT(AVG(FTemperature), 1) as FTemperature, FORMAT(AVG(FHumidity), 1) as FHumidity, FORMAT(AVG(FNoise), 1) as FNoise, FORMAT(AVG(FNoiseMax), 1) as FNoiseMax  FROM T_EnvdetectionHisData WHERE FTimestamp BETWEEN '"+ begin_time +"' and '"+ end_time +"' group by FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i')"
            cur.execute(sqlstr)

            rows = dictfetchall(cur)

            data_pm25 = rows[0]['FPM25']
            data_pm10 = rows[0]['FPM10']
            data_spm = rows[0]['FSPM']
            data_FWIND_SPEED = rows[0]['FWIND_SPEED']
            data_FTemperature = rows[0]['FTemperature']
            data_FHumidity = rows[0]['FHumidity']
            data_FNoise = rows[0]['FNoise']
            data_FNoiseMax = rows[0]['FNoiseMax']
            data_FWIND_DIRECT_STR = ''
        else:
            device_info = device.objects.filter(Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a'), Q(CREATED_PRJ=prjID)).first()
            realtime_data = envinterfacesrv.objects.filter(Q(FDeviceId=device_info.FDevID)).order_by('-FTimestamp').first()

            data_pm25 = realtime_data.FPM25
            data_pm10 = realtime_data.FPM10
            data_spm = realtime_data.FSPM
            data_FWIND_SPEED = realtime_data.FWIND_SPEED
            data_FTemperature = realtime_data.FTemperature
            data_FHumidity = realtime_data.FHumidity
            data_FNoise = realtime_data.FNoise
            data_FNoiseMax = realtime_data.FNoiseMax
            data_FWIND_DIRECT_STR = realtime_data.FWIND_DIRECT_STR

        response_data = []

        dict = {}
        dict['value'] = data_pm25
        dict['name'] = 'PM2.5'
        dict['itemStyle'] = {'color': '#FFB24E'}
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_pm10
        dict['name'] = 'PM10'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_spm
        dict['name'] = 'SPM'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_FWIND_SPEED
        dict['name'] = '风速'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_FTemperature
        dict['name'] = '温度'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_FHumidity
        dict['name'] = '湿度'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_FNoise
        dict['name'] = '噪音'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_FNoiseMax
        dict['name'] = '噪音峰值'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = data_FWIND_DIRECT_STR
        dict['name'] = '风向文字'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        return HttpResponse(json.dumps(response_data))
        #return JsonResponse(response_data, safe=False)


class get_envhisdata(View):
    def post(self, request):
        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        begin_time = (datetime.datetime.now() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")

        prjID = ''.join(str(request.POST.get('prjid')).split('-'))

        cur = connection.cursor()
        sqlstr = "SELECT FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i'), format(avg(FPM25), 1) from T_EnvdetectionHisData where CREATED_PRJ like '%"+ prjID +"%' and FTimestamp BETWEEN '"+ begin_time +"' and '"+ end_time +"' group by FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i')"

        cur.execute(sqlstr)

        rows = cur.fetchall()

        response_days = []
        response_pm25 = []
        response_pm10 = []


        for r in rows:
            response_days.append(r[0])
            response_pm25.append(r[1])


        cur1 = connection.cursor()
        sqlstr = "SELECT FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i'), format(avg(FPM10), 1) from T_EnvdetectionHisData where CREATED_PRJ like '%"+ prjID +"%' and FTimestamp BETWEEN '"+ begin_time +"' and '"+ end_time +"' group by FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i')"

        cur1.execute(sqlstr)
        rows1 = cur1.fetchall()

        for r1 in rows1:
            response_pm10.append(r1[1])


        result_dict = {'FDay': response_days, 'FPM25': response_pm25, 'FPM10': response_pm10}
        cur.close()
        cur1.close()
        return JsonResponse(result_dict, safe=False)


class get_area_analyse(View):
    def post(self, request):
        cur = connection.cursor()

        sqlstr = "SELECT * FROM cc_region WHERE parent_id=360100 ORDER BY id"
        cur.execute(sqlstr)
        rows = cur.fetchall()

        area_data = []
        area_prj_data = []
        area_pm25_data = []
        area_pm10_data = []
        area_noise_data = []
        area_temp_data = []
        area_hum_data = []

        for r in rows:
            area_data.append(r[1])
            project_count = project.objects.filter(Q(FStatus=True), Q(areaid=r[0])).count()
            area_prj_data.append(project_count)

            cur1 = connection.cursor()
            sqlstr = "SELECT c.id, FORMAT(avg(a.FPM25),1), FORMAT(avg(a.FPM10),1), FORMAT(avg(a.FNoise),1), FORMAT(avg(a.FTemperature),1), FORMAT(avg(a.FHumidity),1) FROM T_EnvdetectionHisData AS a LEFT JOIN  T_Project as b on a.CREATED_PRJ=b.FID LEFT JOIN cc_region as c ON b.areaid=c.id WHERE c.id="+str(r[0])+" GROUP BY c.id"
            cur1.execute(sqlstr)
            row_pm = cur1.fetchall()

            if len(row_pm) == 0:
                area_pm25_data.append(0)
                area_pm10_data.append(0)
                area_noise_data.append(0)
                area_temp_data.append(0)
                area_hum_data.append(0)
            else:
                area_pm25_data.append(row_pm[0][1])
                area_pm10_data.append(row_pm[0][2])
                area_noise_data.append(row_pm[0][3])
                area_temp_data.append(row_pm[0][4])
                area_hum_data.append(row_pm[0][5])

            cur1.close()

        result_dict = {"areadata": area_data, "prjdata": area_prj_data, "pm25data": area_pm25_data, "pm10data": area_pm10_data, "noisedata": area_noise_data, "tempdata": area_temp_data, "humdata": area_hum_data }
        return JsonResponse(result_dict, safe=False)


class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        self.orgsplit_type = 1
        self.type = 2

        cur = connection.cursor()

        sqlstr = "SELECT c.name, b.FPrjname, FORMAT( avg( a.FPM25 ), 1 ) AS pm25, format( avg( a.FPM10 ), 1 ) AS pm10, FORMAT( avg( a.FNoise ), 1 ) AS noise FROM T_EnvdetectionHisData AS a LEFT JOIN T_Project AS b ON a.CREATED_PRJ = b.FID LEFT JOIN cc_region AS c ON b.areaid = c.id  WHERE c.parent_id = 360100 GROUP BY c.name, a.CREATED_PRJ ORDER BY pm25 DESC"
        cur.execute(sqlstr)
        rows = dictfetchall(cur)

        return rows



#万物互联升降机监测
class elevatorcockpit_entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/datacockpit/elevatorcockpit.html'

        elevator_info = device.objects.filter(Q(FDevtypeID='af2cecf8bd6811e987267831c1d24216'))

        self.context['elevator_count'] = elevator_info.count()
        self.context['enable_count'] = elevator_info.filter(Q(FStatus=True))
        self.context['disable_count'] = elevator_info.filter(Q(FStatus=False))

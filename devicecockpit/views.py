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

class envcockpit_entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/datacockpit/devcockpit.html'

        device_info = device.objects.filter(Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a'))

        self.context['envdev_count'] = device_info.count()
        self.context['enable_count'] = device_info.filter(Q(FStatus=True))
        self.context['disable_count'] = device_info.filter(Q(FStatus=False))


class get_envrealtimedata(View):
    def post(self, request):
        prjID = request.POST.get('prjid')

        if prjID == '':
            device_info = device.objects.filter(Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a')).first()
        else:
            device_info = device.objects.filter(Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a'), Q(CREATED_PRJ=prjID)).first()

        realtime_data = envinterfacesrv.objects.filter(Q(FDeviceId=device_info.FDevID)).order_by('-FTimestamp').first()
        response_data = []

        dict = {}
        dict['value'] = realtime_data.FPM25
        dict['name'] = 'PM2.5'
        dict['itemStyle'] = {'color': '#FFB24E'}
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FPM10
        dict['name'] = 'PM10'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FSPM
        dict['name'] = 'SPM'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FWIND_SPEED
        dict['name'] = '风速'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FTemperature
        dict['name'] = '温度'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FHumidity
        dict['name'] = '湿度'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FNoise
        dict['name'] = '噪音'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        dict = {}
        dict['value'] = realtime_data.FNoiseMax
        dict['name'] = '噪音峰值'
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}
        response_data.append(dict)

        return HttpResponse(json.dumps(response_data))
        #return JsonResponse(response_data, safe=False)


class get_envhisdata(View):
    def post(self, request):
        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        begin_time = (datetime.datetime.now() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")

        prjID = request.POST.get('prjid')

        cur = connection.cursor()
        sqlstr = "SELECT FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i'), format(avg(FPM25), 1) from T_EnvdetectionHisData where CREATED_PRJ='"+ prjID +"' and FTimestamp BETWEEN '"+ begin_time +"' and '"+ end_time +"' group by FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i')"

        cur.execute(sqlstr)

        rows = cur.fetchall()

        response_days = []
        response_pm25 = []
        response_pm10 = []


        for r in rows:
            response_days.append(r[0])
            response_pm25.append(r[1])


        cur1 = connection.cursor()
        sqlstr = "SELECT FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i'), format(avg(FPM10), 1) from T_EnvdetectionHisData where CREATED_PRJ='"+ prjID +"' and FTimestamp BETWEEN '"+ begin_time +"' and '"+ end_time +"' group by FROM_UNIXTIME(FSRCTimestamp-FSRCTimestamp % (60*60), '%m-%d %H:%i')"

        cur1.execute(sqlstr)
        rows1 = cur1.fetchall()

        for r1 in rows1:
            response_pm10.append(r1[1])


        result_dict = {'FDay': response_days, 'FPM25': response_pm25, 'FPM10': response_pm10}

        return JsonResponse(result_dict, safe=False)



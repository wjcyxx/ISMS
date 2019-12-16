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
        pass
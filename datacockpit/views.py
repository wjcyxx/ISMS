from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q, Sum, Count
from basedata.models import base
from organize.models import organize
from project.models import project
from device.models import device
from personnel.models import personnel
from pedpassage.models import passagerecord
from personauth.models import personauth
from devinterfacesrv.models import envinterfacesrv
from device.models import device
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

class get_datacockpit(View):
    def post(self, request):
        org_type = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))

        response_data = []
        for obj in org_type:
            dict = {}

            fid = ''.join(str(obj.FID).split('-'))
            name = obj.FBase

            org_count = organize.objects.filter(Q(FStatus=True), Q(FOrgtypeID=fid)).count()
            if org_count == 0:
                org_count = None

            dict['value'] = org_count
            dict['name'] = name
            #dict['itemStyle'] = {'color': '#FFB24E'}
            dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}

            response_data.append(dict)

        org_disable_count = organize.objects.filter(Q(FStatus=False)).count()
        if org_disable_count == 0:
            org_disable_count = None

        dict = {}
        dict['value'] = org_disable_count
        dict['name'] = '禁用组织'
        dict['itemStyle'] = {'color': '#999999'}
        dict['label'] = {'fontSize': 30, 'color': '#999999'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)



class get_prjcockpit(View):
    def post(self, request):
        prj_type = base.objects.filter(Q(FPID='4a94b19ea3d811e9b984708bcdb9b39a'))

        response_data = []
        for obj in prj_type:
            dict = {}

            fid = ''.join(str(obj.FID).split('-'))
            name = obj.FBase

            prj_count = project.objects.filter(Q(FStatus=True), Q(FPrjtypeID=fid)).count()

            if prj_count == 0:
                prj_count = None

            dict['value'] = prj_count
            dict['name'] = name
            dict['itemStyle'] = {'color': '#FFB24E'}
            dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}

            response_data.append(dict)

        prj_disable_count = project.objects.filter(Q(FStatus=False)).count()

        if prj_disable_count == 0:
            prj_disable_count = None

        dict = {}
        dict['value'] = prj_disable_count
        dict['name'] = '禁用项目'
        dict['itemStyle'] = {'color': '#999999'}
        dict['label'] = {'fontSize': 30, 'color': '#999999'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)


class get_prjstatus(View):
    def post(self, request):
        prj_status = base.objects.filter(Q(FPID='22682ae6a3da11e9920c708bcdb9b39a')).order_by('FBaseID')

        response_data = []
        for obj in prj_status:
            dict = {}

            fid = ''.join(str(obj.FID).split('-'))
            name = obj.FBase

            prj_count = project.objects.filter(Q(FPrjstate=fid)).count()

            dict['value'] = prj_count
            dict['name'] = name
            dict['itemStyle'] = {'color': '#F1B561'}

            response_data.append(dict)


        return JsonResponse(response_data, safe=False)

class get_prjcost(View):
    def post(self, request):

        response_data = []

        prj_cost = project.objects.filter(Q(FStatus=True)).values('FPrjtypeID').annotate(cost=Sum('FPrjcost'))

        for prjcost in prj_cost:
            dict = {}

            if prjcost['cost'] == 0:
                dict['value'] = None
            else:
                dict['value'] = prjcost['cost']

            prjtype = base.objects.get(Q(FID=prjcost['FPrjtypeID'])).FBase
            dict['name'] = prjtype
            dict['itemStyle'] = {'color': '#FFB24E'}
            #dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}

            response_data.append(dict)

        return JsonResponse(response_data, safe=False)

class get_iotdev(View):
    def post(self, request):
        dev_type = base.objects.filter(Q(FPID='8feb17b2aaf211e99741708bcdb9b39a'))

        response_data = []

        for obj in dev_type:
            dict = {}

            fid = ''.join(str(obj.FID).split('-'))
            name = obj.FBase

            dev_count = device.objects.filter(Q(FStatus=True), Q(FDevtypeID=fid)).count()

            if dev_count == 0:
                dev_count = None

            dict['value'] = dev_count
            dict['name'] = name
            #dict['itemStyle'] = {'color': '#FFB24E'}
            dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}

            response_data.append(dict)

        dev_disable_count = device.objects.filter(Q(FStatus=False)).count()

        if dev_disable_count == 0:
            dev_disable_count = None

        dict = {}
        dict['value'] = dev_disable_count
        dict['name'] = '禁用设备'
        dict['itemStyle'] = {'color': '#999999'}
        dict['label'] = {'fontSize': 30, 'color': '#999999'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)


class get_personregcount(View):
    def post(self, request):
        response_data = []

        reg_count = personnel.objects.filter(Q(FStatus=0), ~Q(FType=0)).count()

        dict = {}
        dict['value'] = reg_count
        dict['name'] = '在册人员'
        dict['itemStyle'] = {'color': '#A7FFFD'}
        dict['label'] = {'fontSize': 30, 'color': '#FFB24E'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)



class get_personquitcount(View):
    def post(self, request):
        response_data = []

        quit_count = personnel.objects.filter(Q(FStatus=1), ~Q(FType=0)).count()

        dict = {}
        dict['value'] = quit_count
        dict['name'] = '退场人员'
        dict['itemStyle'] = {'color': '#A7FFFD'}
        dict['label'] = {'fontSize': 30, 'color': '#FFB24E'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)


class get_personsitcount(View):
    def post(self, request):
        response_data = []

        sit_count = passagerecord.objects.filter(Q(CREATED_TIME__year=timezone.now().year), Q(CREATED_TIME__month=timezone.now().month), Q(CREATED_TIME__day=timezone.now().day)).values('FPersonID').annotate(total=Count('FPersonID'))

        dict = {}
        dict['value'] = len(sit_count)
        dict['name'] = '在场人员'
        dict['itemStyle'] = {'color': '#A7FFFD'}
        dict['label'] = {'fontSize': 30, 'color': '#FFB24E'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)


class get_personauthcount(View):
    def post(self, request):
        response_data = []

        auth_count = personauth.objects.all().values('FPersonID').annotate(total=Count('FPersonID'))

        dict = {}
        dict['value'] = len(auth_count)
        dict['name'] = '授权人员'
        dict['itemStyle'] = {'color': '#A7FFFD'}
        dict['label'] = {'fontSize': 30, 'color': '#FFB24E'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)


class get_citypm(View):
    def post(self, request):

        initID = '7698fa5e195b11eaad2facde48001122'
        city_pm = get_interface_result(initID)

        initID = 'cccc50ca195f11ea8c4aacde48001122'
        city_weather = get_interface_result(initID)

        response_data = {}

        response_data['pm25'] = city_pm['pm25']
        response_data['pm10'] = city_pm['pm10']
        response_data['aqi'] = city_pm['aqi']
        response_data['level'] = city_pm['level']
        response_data['temp'] = city_weather['temp']
        response_data['weather'] = city_weather['weather']
        response_data['wd'] = city_weather['wd']
        response_data['wdforce'] = city_weather['wdforce']
        response_data['wdspd'] = city_weather['wdspd']

        return HttpResponse(json.dumps(response_data))


class get_mapdata(View):
    def post(self, request):
        response_data = []

        prj_info = project.objects.filter(Q(FStatus=True))

        for obj in prj_info:
            dict = {}
            fid = ''.join(str(obj.FID).split('-'))

            dict['latitude'] = obj.FLat
            dict['longitude'] = obj.FLong
            dict['name'] = obj.FPrjname
            dict['value'] = fid

            type = request.POST.get('type')

            if type == '2':     #万物互联，电梯页面地图点颜色
                elevator_count = device.objects.filter(Q(CREATED_PRJ=fid), Q(FDevtypeID='af2cecf8bd6811e987267831c1d24216')).count()

                if elevator_count > 0:
                    dict['color'] = '#66cc00'
                else:
                    dict['color'] = '#ff0033'

            elif type == '1':   #万物互联，环境页面地图点颜色
                env_info = envinterfacesrv.objects.filter(Q(CREATED_PRJ=fid)).order_by('FTemperature').first()
                if env_info != None:
                    if env_info.FPM25 <= 115:
                        dict['color'] = '#66cc00'
                    elif env_info.FPM25 > 115 and env_info.FPM25 <= 150:
                        dict['color'] = '#ffff00'
                    elif env_info.FPM25 > 150 and env_info.FPM25 <= 250:
                        dict['color'] = '#d94d02'
                    elif env_info.FPM25 > 250 and env_info.FPM25 <= 500:
                        dict['color'] = '#ff0033'
                else:
                    dict['color'] = '#66cc00'

            elif type == '0':   #数据驾驶舱首页，地图点默认颜色
                dict['color'] = '#d94d02'

            response_data.append(dict)

        return HttpResponse(json.dumps(response_data))









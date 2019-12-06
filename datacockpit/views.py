from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q, Sum
from basedata.models import base
from organize.models import organize
from project.models import project
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
            dict['itemStyle'] = {'color': '#FFB24E'}
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
        prj_type = base.objects.filter(Q(FPID='4a94b19ea3d811e9b984708bcdb9b39a'))

        response_data = []

        for obj in prj_type:
            dict = {}

            fid = ''.join(str(obj.FID).split('-'))
            name = obj.FBase

            prj_cost = project.objects.filter(Q(FStatus=True), Q(FPrjtypeID=fid)).annotate(cost=Sum('FPrjcost')).values('cost')

            if len(prj_cost) == 0:
                dict['value'] = None
            else:
                dict['value'] = prj_cost[0]['cost']

            dict['name'] = name
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
            dict['itemStyle'] = {'color': '#FFB24E'}
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






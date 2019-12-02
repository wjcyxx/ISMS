from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from basedata.models import base
from organize.models import organize
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
        pass



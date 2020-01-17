from django.shortcuts import render
import urllib.parse
import urllib.request
import hmac
import base64
import hashlib
from hashlib import sha256
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q, Sum, Count
from basedata.models import base
from project.models import project
from devinterfacesrv.models import envinterfacesrv
from common.views import *
from django.http import JsonResponse
from busmenu.models import busmenu
from appkey.models import appkey
from monitordev.models import monitordev
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
from django.db import connection
from django.db.models import Sum, Count
import re

# Create your views here.

class videocockpit_entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/datacockpit/videocockpit.html'

        busmenu_info = busmenu.objects.filter(Q(FPID__isnull=True) | Q(FPID=''), Q(FStatus=True), Q(FMenuPosition=2)).order_by('FSequence')
        self.context['busmenu_info'] = busmenu_info

        video_count = monitordev.objects.all().count()
        self.context['video_count'] = video_count

class get_videocount(View):
    def post(self, request):
        response_data = []

        video_enable_count = monitordev.objects.filter(Q(FStatus=True)).count()
        dict = {}
        dict['value'] = video_enable_count
        dict['name'] = '接入视频设备数量'
        dict['itemStyle'] = {'color': '#FFB24E'}
        dict['label'] = {'fontSize': 30, 'color': '#A7FFFD'}

        response_data.append(dict)

        video_disable_count = monitordev.objects.filter(Q(FStatus=False)).count()
        dict = {}
        dict['value'] = video_disable_count
        dict['name'] = '禁用视频设备数量'
        dict['itemStyle'] = {'color': '#999999'}
        dict['label'] = {'fontSize': 30, 'color': '#999999'}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)


class get_prjcount(View):
    def post(self, request):
        response_data = []

        prj_video_count = monitordev.objects.all().values('CREATED_PRJ').distinct().count()
        dict = {}
        dict['value'] = prj_video_count
        dict['name'] = '已接入视频项目数量'
        #dict['itemStyle'] = {'color': '#FFB24E'}
        dict['label'] = {'fontSize': 30}

        response_data.append(dict)

        prj_count = project.objects.filter(Q(FStatus=True)).count()
        dict = {}
        dict['value'] = prj_count
        dict['name'] = '所有项目数量'
        #dict['itemStyle'] = {'color': '#FFB24E'}
        dict['label'] = {'fontSize': 30}

        response_data.append(dict)

        return JsonResponse(response_data, safe=False)



class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        self.orgsplit_type = 1
        self.type = 2

        serinput = self.request.GET.get("resultdict[CREATED_PRJ]", '')

        cur = connection.cursor()

        sqlstr = "SELECT A.*, B.FPrjname, B.FAddress FROM ISMS.T_MonitorDev AS A LEFT JOIN ISMS.T_Project AS B ON A.CREATED_PRJ=B.FID WHERE A.FStatus=TRUE AND B.FPrjname LIKE '%"+ serinput +"%' ORDER BY B.FPrjname, A.FChannel"
        cur.execute(sqlstr)
        rows = dictfetchall(cur)

        return rows


class get_videourl(View):
    def post(self, request):
        response_data = {}

        try:
            devinterface_info = devinterface.objects.get(Q(FScope=1), Q(FCallSigCode='GETVIDEOURL'))

            initID = ''.join(str(devinterface_info.FID).split('-'))
            APPFID = devinterface_info.FAppFID
            app_info = appkey.objects.get(Q(FID=APPFID))

            APPKEY = app_info.FAppkey
            APPSECRET = app_info.FAppSecret.encode('utf-8')
            #DATE = timezone.now().strftime('%Y-%m-%d')
            DATE = '2020-01-15'
            URL = '/artemis/api/video/v1/cameras/previewURLs'

            mvideo = metro_video()
            SIGNATURE = mvideo.get_sign(APPKEY, APPSECRET, DATE, URL)

            DEV_ID = request.POST.get('devid')

            video_result = get_interface_result(initID, [DEV_ID], [DATE, APPKEY, SIGNATURE], [])

            response_data['result'] = video_result['code']
            response_data['msg'] = video_result['msg']
            if video_result['code'] == '0':
                response_data['url'] = video_result['data']['url']

            return HttpResponse(json.dumps(response_data))
        except Exception as e:
            response_data['result'] = 1
            response_data['msg'] = str(e)

            return HttpResponse(json.dumps(response_data))


class metro_video():
    def get_sign(self, appkey, appsecret, date, url):

        data = str("POST" + "\n" + "*/*" + "\n" + "application/json" + "\n" + date + "\n" + "x-ca-key" + ":" + appkey + "\n" + url).encode('utf-8')

        signature = str(base64.b64encode(hmac.new(appsecret, data, digestmod=sha256).digest()), encoding="utf-8")

        return signature


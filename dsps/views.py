from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import dsps as T_MonitorPoint
from basedata.models import base
from device.models import device
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from django.core.cache import cache
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/dsps/dspsinfo.html'

        initID = '2e8bc6eaf0b311e985c3a860b624be51'
        token = get_interface_result(initID)['token']

        initID = 'de9dc834f15411e998f0a860b624be51'
        scheme = get_interface_result(initID, [], [token])

        self.request.session['gzmtoken'] = token

        if scheme['result'] == 0:
            self.context['schemename'] = scheme['plan_names']


#返回table数据及查询结果
class get_datasource(View):
    def get(self, request):
        schemeid = request.GET.get('schemeid')
        daterage = request.GET.get('daterage')

        datelist = str(daterage).split(' - ')
        begindate = datelist[0]
        enddate = datelist[1]

        initID = '83de3730f3b611e986ab7831c1d24216'
        token = request.session['gzmtoken']

        data = get_interface_result(initID, [schemeid, begindate, enddate], [token])
        if data['result'] == 0:
            resultdict = {'code':0, 'msg':"", 'count': len(data['datas']), 'data': data['datas']}

            return JsonResponse(resultdict, safe=False)


#链接采集设备配置信息view
class dev_setupinfo(EntranceView_base):
    def set_view(self, request):
        devid = self.request.GET.get('devid')
        schemeid = self.request.GET.get('schemeid')

        self.template_name = 'content/dsps/devsetupinfo.html'
        self.context['devid'] = devid
        self.context['schemeid'] = schemeid


#返回采集器配置信息table
class get_dev_datasource(View):
    def get(self, request):
        devid = request.GET.get('devid')
        schemeid = request.GET.get('schemeid')

        token = request.session['gzmtoken']
        initID = '3fd972a6f62d11e98f35a860b624be51'

        data = get_interface_result(initID, [schemeid], [token])

        if data['result'] == 0:
            data_info = data['l']

            for obj in data_info:
                if str(obj['i']) == devid:
                    data = []
                    a1 = {'title': '预警值', 'a': obj['a1']}
                    data.append(a1)

                    a2 = {'title': '报警值', 'a': obj['a2']}
                    data.append(a2)

                    a3 = {'title': '控制值', 'a': obj['a3']}
                    data.append(a3)

                    resultdict = {'code':0, 'msg':"", 'count': 3, 'data': data}
                    break

            return JsonResponse(resultdict, safe=False)


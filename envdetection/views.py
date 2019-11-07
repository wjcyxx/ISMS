from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
# Create your views here.


#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):

        initID = 'b93df570c31c11e982a27831c1d24216'

        url = get_interface_url(initID)
        param = get_interface_param(initID)

        req = url + '?' + param

        response = urllib.request.urlopen(req)
        data = response.read()
        data = data.decode('utf-8')

        result = json.loads(data)

        i = 0
        j = 0
        for obj in result:
            if obj['DevStatus'] == 'false':
                i += 1

            if (obj['HumiStatus'] != '0') or (obj['TempStatus'] != '0'):
                j += 1


        #self.template_name = 'content/envdetection/envdetectioninfo.html'
        self.template_name = 'content/envdetection/envvisual.html'
        self.context['devinfo'] = result
        self.context['count'] = len(result)
        self.context['online'] = len(result) - i
        self.context['alert'] = j
        self.context['offline'] = i

#返回table数据及查询结果
class get_datasource(View):

    def post(self, request):

        initID = 'b93df570c31c11e982a27831c1d24216'

        url = get_interface_url(initID)
        param = get_interface_param(initID)

        req = url + '?' + param

        response = urllib.request.urlopen(req)
        data = response.read()
        data = data.decode('utf-8')

        result = json.loads(data)

        dict = {}
        for dt in result:
            if dt['DevName'] == 'PM':
                dict['PM10'] = dt['DevTempValue']
                dict['PM2.5'] = dt['DevHumiValue']

            elif dt['DevName'] == '噪声':
                dict['ZS'] = dt['DevHumiValue']

            elif dt['DevName'] == '温度湿度':
                dict['WD'] = dt['DevTempValue']
                dict['SD'] = dt['DevHumiValue']


        return JsonResponse(dict, safe=False)



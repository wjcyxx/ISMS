from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from .models import envdatalog as T_EnvDataLog
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import urllib.parse
import re
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

        self.template_name = 'content/envdatalog/envdataloginfo.html'
        self.context['devinfo'] = result


#返回table数据及查询结果
class get_datasource(View):

    def get(self, request):

        initID = 'b93df570c31c11e982a27831c1d24216'

        url = get_interface_url(initID)
        param = get_interface_param(initID)

        req = url + '?' + param

        response = urllib.request.urlopen(req)
        data = response.read()
        data = data.decode('utf-8')

        result = json.loads(data)

        serinput = request.GET.get("resultdict[DevKey]", '')

        if serinput != '':
            data = []
            for obj in result:
                if obj['DevKey'] == serinput:
                    result = obj
                    data.append(result)
                    break

            resultdict = {'code':0, 'msg':"", 'count': len(result), 'data': data}
        else:
            resultdict = {'code':0, 'msg':"", 'count': len(result), 'data': result}


        return JsonResponse(resultdict, safe=False)

#返回历史数据table数据及查询结果
class get_hislog_datasource(View):
    def get(self, request):

        devKey = request.GET.get('devkey')
        devdate = str(request.GET.get('devdate')).split(' - ')
        devdate[0] = devdate[0].replace('-', '') + '0000'
        devdate[1] = devdate[1].replace('-', '') + '2359'

        params = [devKey, devdate[0], devdate[1]]

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
        resultdict = {'code':0, 'msg':"", 'count': len(result), 'data': result['HisData']}

        return JsonResponse(resultdict, safe=False)

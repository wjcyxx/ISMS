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
        self.template_name = 'content/elevator/elevatorinfo.html'


class get_datasource(View):
    def get(self, request):
        initID = 'cdc1cf78cf8111e9af1d7831c1d24216'

        token = get_interface_result(initID)['data']['token']
        request.session['mectoken'] = token

        initID = '7293af48cfab11e9b5c17831c1d24216'
        result = get_interface_result(initID, [token])['data']

        resultdict = {'code':0, 'msg':"", 'count': len(result), 'data': result}

        return JsonResponse(resultdict, safe=False)


class get_run_datasource(View):
    def get(self, request):
        box_id = request.GET.get('boxid')

        initID = 'cdc1cf78cf8111e9af1d7831c1d24216'
        token = get_interface_result(initID)['data']['token']

        initID = 'b49d3f2ed04d11e9b9dd7831c1d24216'
        result = get_interface_result(initID, [token, box_id])['data']

        resultdict = {'code':0, 'msg':"", 'count': len(result), 'data': result}
        return JsonResponse(resultdict, safe=False)






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
# Create your views here.


#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/envdatalog/envdataloginfo.html'


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FNodename]", '')
        envdatalog_info =  T_EnvDataLog.objects.filter(Q(CREATED_PRJ=prj_id), Q(FNodename__contains=serinput))

        return envdatalog_info

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import hatalertlog as T_HatAlertLog
from area.models import area
from group.models import group
from team.models import team
from basedata.models import base
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from django.views.generic import View
# Create your views here.

#控制器入口
class enterance(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/hatalertlog/hatalertinfo.html'
        self.query_sets = [
            area.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
        ]
        self.quer_set_fieldnames = ['FName', 'FName', 'FGroup', 'FBase']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        self.type = 1
        prj_id = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FPersonID__FName]", '')
        hatalertlog_info =  T_HatAlertLog.objects.filter(Q(FPersonID__FName__contains=serinput), Q(CREATED_PRJ=prj_id)).values('FPersonID__FName', 'FPersonID__FTeamID','FPersonID__FGroupID', 'FPersonID__FWorktypeID', 'FRuleID__FAreaID', 'FPicPath', 'CREATED_TIME' )

        return hatalertlog_info

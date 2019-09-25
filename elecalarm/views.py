from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from .models import elecalarm as T_ElecAlarm
from elecfencle.models import elecfencle
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
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/elecalarm/elecalarminfo.html'
        self.query_sets = [
            elecfencle.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
        ]
        self.quer_set_fieldnames = ['FElecFence']


class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']

        serinput = self.request.GET.get("resultdict[FPlate]", '')
        elecalarm_info =  T_ElecAlarm.objects.filter(Q(CREATED_PRJ=prj_id), Q(FPlate__contains=serinput))

        return elecalarm_info


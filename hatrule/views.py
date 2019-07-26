from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import hatrule as T_HatRule
from device.models import device
from area.models import area
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from django.views.generic import View
# Create your views here.

query_sets = []


class hatrule(EntranceView_base):
    def set_view(self, request):
        global query_sets
        query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']))
        ]

        self.template_name = 'content/hatrule/hatruleinfo.html'
        self.query_sets = query_sets
        self.quer_set_fieldnames = ['FDevice', 'FName']


class get_datasource(get_datasource_base):
    def get_queryset(self, request):
        prjid = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FRule]", '')
        hatrule_info = T_HatRule.objects.filter(Q(CREATED_PRJ=prjid), Q(FRule__contains=serinput))

        return hatrule_info

class add(add_base):
    def set_view(self, request):
        global query_sets

        self.template_name = 'content/hatrule/hatruleadd.html'
        self.objForm = HatRuleModelForm()
        self.query_sets = query_sets
        self.query_set_idfields = [
            'FDevID', 'FAreaID'
        ]
        self.query_set_valuefields = [
            'FDevice', 'FName'
        ]





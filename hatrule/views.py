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


class hatrule(EntranceView_base):
    def set_view(self, request):
        query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
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
        self.template_name = 'content/hatrule/hatruleadd.html'
        self.objForm = HatRuleModelForm()
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']

class edit(edit_base):
    def set_view(self, request):
        self.template_name = 'content/hatrule/hatruleadd.html'
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))
        self.model = T_HatRule.objects.get(Q(FID=fid))
        self.objForm = HatRuleModelForm(instance=self.model)
        self.query_sets = [
            device.objects.filter(Q(FStatus=True)),
            area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
        ]
        self.query_set_idfields = ['FDevID', 'FAreaID']
        self.query_set_valuefields = ['FDevice', 'FName']


class insert(insert_base):
    def set_view(self, request):
        try:
            if self.request.GET.get('actype') == 'insert':
                self.objForm = HatRuleModelForm(self.request.POST)
            elif self.request.GET.get('actype') == 'update':
                fid = self.request.POST.get('FID')
                self.model = T_HatRule.objects.get(Q(FID=fid))
                self.objForm = HatRuleModelForm(self.request.POST, instance=self.model)
            else:
                self.response_data['result'] = '2'

            self.query_sets = [
                device.objects.filter(Q(FStatus=True)),
                area.objects.filter(Q(CREATED_PRJ=self.request.session['PrjID']), Q(FStatus=True))
            ]
            self.query_set_idfields = ['FDevID', 'FAreaID']
            self.query_set_valuefields = ['FDevice', 'FName']
        except Exception as e:
            erorr = e







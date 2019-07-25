from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.db import models
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

# Create your views here.

#global req

class EntranceView(View):
    template_name = ''
    query_sets = []
    quer_set_fieldnames = []
    context = []

    @login_decorator
    def get(self, request, *args):
        return render(self.request, self.template_name, self.set_context(self) )

    def post(self, request):
        pass

    def set_context(self, request):

        if len(self.query_sets) == len(self.quer_set_fieldnames):
            for obj in self.query_sets:
                dict = {}
                #dict[] get_dict_table

        else:
            pass


class get_datasource(View):
    request = None

    def get(self, request):
        pass

    def post(self, request):
        try:
            self.request = request
            query_set = self.get_queryset(self)
            dict = convert_to_dicts(query_set)
            resultdict = {'code':0, 'msg':"", 'count': query_set.count(), 'data': dict}

            return  JsonResponse(resultdict, safe=False)
        except  Exception as e:
            return  e

    def get_queryset(self, reqeust):
        pass

class add(View):
    template_name = ''
    context = {}

    def get(self, request):
        pass

    def post(self, request):
        pass
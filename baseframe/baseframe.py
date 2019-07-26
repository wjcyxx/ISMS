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
import requests

# Create your views here.

class EntranceView_base(View):
    template_name = ''
    query_sets = []
    quer_set_fieldnames = []
    context = {}
    request = None

    @login_decorator
    def get(self, request, *args):
        self.request = request
        self.set_view(self)
        return render(self.request, self.template_name,  self.set_context(self))

    def post(self, request):
        pass

    def set_view(self, request):
        pass

    def set_context(self, request):

        if len(self.query_sets) == len(self.quer_set_fieldnames):
            for i in range(len(self.query_sets)):

                 self.context[self.query_sets[i].model.__name__] = get_dict_table(self.query_sets[i] , 'FID', self.quer_set_fieldnames[i])

            return self.context

        else:
            pass


class get_datasource_base(View):
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

class add_base(View):
    template_name = ''
    objForm = None
    query_sets = []
    query_set_idfields = []
    query_set_valuefields = []
    context = {}
    request = None

    def get(self, request):
        self.request = request
        self.set_view(self)
        if len(self.query_sets) > 0:
            self.ref_dropdown(self)

        self.context = {'obj': self.objForm, 'action': 'insert'}

        return render(self.request, self.template_name,  self.context)

    def post(self, request):
        pass

    def ref_dropdown(self, request):
        if len(self.query_sets) == len(self.query_set_idfields) and len(self.query_set_idfields)== len(self.query_set_valuefields):
            for i in range(len(self.query_sets)):
                self.objForm.fields[self.query_set_idfields[i]].choices = get_dict_object(request, self.query_sets[i], 'FID', self.query_set_valuefields[i])
        else:
            pass

    def set_view(self, request):
        pass

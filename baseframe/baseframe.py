from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import QuerySet
from django.db import models
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

# Create your views here.

class EntranceView_base(View):
    template_name = ''
    query_sets = []
    quer_set_fieldnames = []
    param_sets = []
    param_value = []
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
                if isinstance(self.query_sets[i], QuerySet):
                    self.context[self.query_sets[i].model.__name__] = get_dict_table(self.query_sets[i] , 'FID', self.quer_set_fieldnames[i])
                else:
                    self.context[self.query_sets[i]] = self.quer_set_fieldnames[i]

        return self.context

class get_datasource_base(View):
    request = None
    type = 0

    def get(self, request):
        try:
            self.request = request
            query_set = self.get_queryset(self)
            if self.type == 0:
                dict = convert_to_dicts(query_set)
            else:
                dict = list(query_set)

            resultdict = {'code':0, 'msg':"", 'count': query_set.count(), 'data': dict}

            return  JsonResponse(resultdict, safe=False)
        except  Exception as e:
            return  e

    def post(self, request):
        pass

    def get_queryset(self, reqeust):
        pass

class add_base(View):
    template_name = ''
    objForm = None
    obj = None
    query_sets = []
    query_set_idfields = []
    query_set_valuefields = []
    context = {}
    request = None

    def get(self, request):
        self.request = request
        self.set_view(self)

        self.obj = self.objForm()

        if len(self.query_sets) > 0:
            self.ref_dropdown(self)

        self.context['obj'] = self.obj
        self.context['action'] = 'insert'

        return render(self.request, self.template_name,  self.context)

    def post(self, request):
        pass

    def ref_dropdown(self, request):
        if len(self.query_sets) == len(self.query_set_idfields) and len(self.query_set_idfields)== len(self.query_set_valuefields):
            for i in range(len(self.query_sets)):
                self.obj.fields[self.query_set_idfields[i]].choices = get_dict_object(request, self.query_sets[i], 'FID', self.query_set_valuefields[i])
        else:
            pass

    def set_view(self, request):
        pass


class edit_base(View):
    template_name = ''
    model = None
    objForm = None
    obj = None
    query_sets = []
    query_set_idfields = []
    query_set_valuefields = []
    context = {}
    request = None

    def get(self, request):
        self.request = request
        self.set_view(self)

        fid = ''.join(str(self.request.GET.get('fid')).split('-'))
        objmodel =  self.model.objects.get(Q(FID=fid))
        self.obj = self.objForm(instance=objmodel)

        self.context['obj'] = self.obj
        self.context['action'] = 'update'

        if len(self.query_sets) > 0:
            self.ref_dropdown(self)


        return render(self.request, self.template_name, self.context)

    def post(self, request):
        pass

    def ref_dropdown(self, request):

        if len(self.query_sets) == len(self.query_set_idfields) and len(self.query_set_idfields)== len(self.query_set_valuefields):
            for i in range(len(self.query_sets)):
                self.obj.fields[self.query_set_idfields[i]].choices = get_dict_object(request, self.query_sets[i], 'FID', self.query_set_valuefields[i])
        else:
            pass

    def set_view(self, request):
        pass


class insert_base(View):
    model = None
    objForm = None
    obj = None
    query_sets = []
    query_set_idfields = []
    query_set_valuefields = []
    request = None
    response_data = {}
    type = 0

    def get(self, request):
        pass

    def post(self, request):
        self.request = request
        self.set_view(self)

        if self.request.GET.get('actype') == 'insert':
            self.obj = self.objForm(self.request.POST)
        elif self.request.GET.get('actype') == 'update':
            fid = self.request.POST.get('FID')
            objmodel = self.model.objects.get(Q(FID=fid))
            self.obj = self.objForm(self.request.POST, instance=objmodel)
        else:
            self.response_data['result'] = '2'


        if len(self.query_sets) > 0:
            self.ref_dropdown(self)

        try:
            if self.obj.is_valid():
                temp = self.obj.save(commit=False)
                if self.request.GET.get('actype') == 'insert':
                    temp.FStatus = True
                if self.type == 1:
                    temp.FPID = self.request.POST.get('FPID')
                temp.CREATED_PRJ = self.request.session['PrjID']
                temp.CREATED_ORG = self.request.session['UserOrg']
                temp.CREATED_BY = self.request.session['UserID']
                temp.UPDATED_BY = self.request.session['UserID']
                temp.CREATED_TIME = timezone.now()

                temp.save()
                self.response_data['result'] = '0'
            else:
                self.response_data['msg'] = self.objForm.errors
                self.response_data['result'] = '1'

            return HttpResponse(json.dumps(self.response_data))

        except Exception as e:
            self.response_data['msg'] = e
            self.response_data['result'] = '1'

            return HttpResponse(json.dumps(self.response_data))

    def ref_dropdown(self, request):
        if len(self.query_sets) == len(self.query_set_idfields) and len(self.query_set_idfields)== len(self.query_set_valuefields):
            for i in range(len(self.query_sets)):
                self.obj.fields[self.query_set_idfields[i]].choices = get_dict_object(request, self.query_sets[i], 'FID', self.query_set_valuefields[i])
        else:
            pass

    def set_view(self, request):
        pass


class disabled_base(View):
    response_data ={}
    model = None
    request = None

    def get(self, request):
        pass

    def post(self, request):
        self.request = request
        self.set_view(self)

        try:
            fid = self.request.POST.get('fid')

            obj = self.model.objects.get(Q(FID=fid))

            if self.request.GET.get('type') == 'lock':
                obj.FStatus = False
            elif self.request.GET.get('type') == 'unlock':
                obj.FStatus = True

            obj.save()

            self.response_data['result'] = '0'
            return HttpResponse(json.dumps(self.response_data))
        except Exception as e:
            self.response_data['result'] = e
            return HttpResponse(json.dumps(self.response_data))


    def set_view(self, request):
        pass


class delete_base(View):
    response_data ={}
    model = None
    request = None

    def get(self, request):
        pass

    def post(self, request):
        self.request = request
        self.set_view(self)

        fid = request.POST.get('fid')

        try:
            self.model.objects.get(FID=fid).delete()
            self.response_data['result'] = '0'
        except:
            self.response_data['result'] = '1'

        return HttpResponse(json.dumps(self.response_data))

    def set_view(self,request):
        pass
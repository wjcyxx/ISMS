from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import QuerySet
from django.db import models
from appkey.models import appkey as T_AppKey
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

    # @login_decorator
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
    orgsplit_type = 0

    def get(self, request):
        try:
            self.request = request
            query_set = self.get_queryset(self)
            if self.orgsplit_type == 0:
                query_set = org_split(query_set, request)

            if self.type == 0:
                dict = convert_to_dicts(query_set)
            elif self.type == 2:
                dict = query_set
            else:
                dict = list(query_set)

            if self.type == 2:
                resultdict = {'code':0, 'msg':"", 'count': len(query_set) , 'data': dict}
            else:
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
    set_fields = []
    set_value = []

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
            beforesave_status = self.set_view_beforesave(self)

            if beforesave_status == 1:

                if self.obj.is_valid():
                    temp = self.obj.save(commit=False)
                    if self.request.GET.get('actype') == 'insert':
                        temp.FStatus = temp.FStatus
                    if self.type == 1:
                        temp.FPID = self.request.POST.get('FPID')
                    temp.CREATED_PRJ = self.request.session['PrjID']
                    temp.CREATED_ORG = self.request.session['UserOrg']
                    temp.CREATED_BY = self.request.session['UserID']
                    temp.UPDATED_BY = self.request.session['UserID']
                    temp.CREATED_TIME = timezone.now()

                    if len(self.set_fields) == len(self.set_value):
                        for i in range(len(self.set_fields)):
                            setattr(temp, self.set_fields[i], self.set_value[i])
                            #temp.field = self.set_value[i]

                    temp.save()
                    self.response_data['result'] = '0'

                    self.set_view_aftersave(self)
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

    def set_view_aftersave(self, request):
        pass

    def set_view_beforesave(self, request):
        return 1

class disabled_base(View):
    response_data ={}
    model = None
    request = None
    type = 0
    status = []

    def get(self, request):
        pass

    def post(self, request):
        self.request = request
        self.set_view(self)

        try:
            fid = self.request.POST.get('fid')

            obj = self.model.objects.get(Q(FID=fid))

            if self.request.GET.get('type') == 'lock':
                if self.type == 0:
                    obj.FStatus = False
                else:
                    obj.FStatus = self.status[0]
            elif self.request.GET.get('type') == 'unlock':
                if self.type == 0:
                    obj.FStatus = True
                else:
                    obj.FStatus = self.status[1]

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

        if self.response_data['result'] == '2':
            return HttpResponse(json.dumps(self.response_data))
        else:
            try:
                self.model.objects.get(FID=fid).delete()
                self.response_data['result'] = '0'
            except:
                self.response_data['result'] = '1'

            return HttpResponse(json.dumps(self.response_data))

    def set_view(self,request):
        pass


class api_base(View):
    response_data = {}
    model = None
    request = None

    def get(self, request):
        self.response_data['result'] = '5'
        self.response_data['msg'] = 'API interface must be submitted by post method.'

        return HttpResponse(json.dumps(self.response_data))

    def post(self, request):
        appkey = request.POST.get('appkey')
        token = request.POST.get('token')
        conditions = request.POST.get('conditions')

        self.request = request
        self.set_view(self)

        if (appkey == None and token == None):
            reqbody = request.body
            request_json = json.loads(reqbody.decode("utf-8"))
            appkey = request_json['appkey']
            token = request_json['token']

        try:
            appkey_info = T_AppKey.objects.get(Q(FAppkey=appkey), Q(FStatus=True))

            self.response_data = certify_token(appkey, token)
            if self.response_data['result'] != '0':
                return HttpResponse(json.dumps(self.response_data))
            else:

                if conditions != None:
                    conditions = json.loads(request.POST.get('conditions'))
                    obj = self.model.objects.filter(**conditions)
                else:
                    obj = self.model.objects.all()

                dict_arr = convert_to_dicts(obj)

                self.response_data['result'] = '0'
                self.response_data['msg'] = 'data returned successfully'
                self.response_data['data'] = dict_arr

                return JsonResponse(self.response_data, safe=False)

        except ObjectDoesNotExist:
            self.response_data['result'] = '4'
            self.response_data['msg'] = 'APIKEY serial is UNREGISTERED'

            return HttpResponse(json.dumps(self.response_data))


    def set_view(self, request):
        pass


class api_common(View):
    response_data = {}
    model = None
    request = None
    data = []

    def get(self, request):
        self.response_data['result'] = '5'
        self.response_data['msg'] = 'API interface must be submitted by post method.'

        return HttpResponse(json.dumps(self.response_data))


    def post(self, request):
        appkey = request.POST.get('appkey')
        token = request.POST.get('token')
        conditions = request.POST.get('conditions')

        self.request = request

        if (appkey == None and token == None):
            reqbody = request.body
            request_json = json.loads(reqbody.decode("utf-8"))
            appkey = request_json['appkey']
            token = request_json['token']

        try:
            appkey_info = T_AppKey.objects.get(Q(FAppkey=appkey), Q(FStatus=True))

            self.response_data = certify_token(appkey, token)
            if self.response_data['result'] != '0':
                return HttpResponse(json.dumps(self.response_data))
            else:
                self.set_view(self)

                # self.response_data['result'] = '0'
                # self.response_data['msg'] = 'data returned successfully'
                # self.response_data['data'] = self.data

                return JsonResponse(self.response_data, safe=False)
        except ObjectDoesNotExist:
            self.response_data['result'] = '4'
            self.response_data['msg'] = 'APIKEY serial is UNREGISTERED'

            return HttpResponse(json.dumps(self.response_data))

    def set_view(self, request):
        pass

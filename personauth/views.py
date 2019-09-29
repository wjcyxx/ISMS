from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from area.models import area
from .models import personauth as T_PersonAuth, personauthmode as T_PersonAuthMode
from personnel.models import personnel
from personnel.models import personnel
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from interface.views import *

def add(request):

    fid = ''.join(str(request.GET.get('fid')).split('-'))
    authtype = request.GET.get('authtype', 0)

    area_info = area.objects.all()
    areadict = get_dict_transfer(area_info, 'FID', 'FName', 'FStatus')

    auth_info = T_PersonAuth.objects.filter(Q(FPersonID=fid))

    dict_auth = []

    for auth in auth_info:
        dict_auth = dict_auth + [str(auth.FAreaID)]

    authList = json.dumps(dict_auth)

    return render(request, "content/personauth/personauthadd.html", {'resultdict' : areadict, 'authList': authList, 'fid': fid, 'authtype': authtype})


def auth(request):
    if request.method == 'POST':
        response_data = {}

        fid = ''.join(str(request.POST.get('fid')).split('-'))
        authtype = request.POST.get('authtype', 0)
        areaid = request.POST.get('areafid')

        area_info =  json.loads(areaid)

        T_PersonAuth.objects.filter(Q(FPersonID=fid)).delete()

        response_data['result'] = '0'
        for obj in area_info:
            personauth_info = T_PersonAuth()
            personauth_info.FPersonID = fid
            personauth_info.FAreaID = obj['value']
            personauth_info.FAuthtype = authtype
            personauth_info.CREATED_PRJ = request.session['PrjID']
            personauth_info.CREATED_ORG = request.session['UserOrg']
            personauth_info.CREATED_BY = request.session['UserID']
            personauth_info.UPDATED_BY = request.session['UserID']
            personauth_info.CREATED_TIME = timezone.now()

            try:
                personauth_info.save()
                response_data['result'] = '0'
            except Exception as e:
                response_data['msg'] = e
                response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))


class makeiccard_add(add_base):
    def set_view(self, request):
        area_info = self.request.GET.get('areainfo')
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        person_info = personnel.objects.get(Q(FID=fid))

        self.template_name = 'content/personauth/makeiccard.html'
        self.objForm = PersonAuthModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='2cd8b28cacf111e991437831c1d24216'))
        ]
        self.query_set_idfields = ['FAuthtypeID']
        self.query_set_valuefields = ['FBase']

        self.context['areainfo'] = json.loads(area_info)
        self.context['person'] = person_info.FName
        self.context['personID'] = fid


class makeiccard(insert_base):
    def set_view(self, request):
        personID = ''.join(str(self.request.GET.get('personID')).split('-'))

        self.model = T_PersonAuthMode
        self.objForm = PersonAuthModelForm

        self.query_sets = [
            base.objects.filter(Q(FPID='2cd8b28cacf111e991437831c1d24216'))
        ]
        self.query_set_idfields = ['FAuthtypeID']
        self.query_set_valuefields = ['FBase']

        self.set_fields = ['FPersonID']
        self.set_value = [personID]

    def set_view_beforesave(self, request):
        result = 0
        areaid = self.request.GET.get('areainfo')
        personID = ''.join(str(self.request.GET.get('personID')).split('-'))

        person_info = personnel.objects.get(Q(FID=personID))

        area_info =  json.loads(areaid)

        for obj_area in area_info:
            passage_inter = areaid_2_device(obj_area['value'])

            if len(passage_inter) == 0:
                continue

            for obj_passage in passage_inter:
                if obj_passage['FExtID'] == '65c7cfb2acf411e991437831c1d24216':  #ICCard注册接口
                    initID = obj_passage['FInterID']
                    initID = ''.join(str(initID).split('-'))

                    person = {"id": personID, "idcardNum": self.request.POST.get('FFeaturevalue'), "name": person_info.FName, "IDNumber": person_info.FIDcard, "facePermission": 2, "idCardPermission": 2, "faceAndCardPermission": 2, "IDPermission": 2}

                    person = json.dumps(person)

                    #result = get_interface_result(initID, [person])['result']
                    result = 1

                    if result != 1:
                        break


                if self.request.POST.get('FAuthvalidity') != '':
                    if obj_passage['FExtID'] == '43b9c462e28111e9a9d27831c1d24216':
                        initID = obj_passage['FInterID']
                        initID = ''.join(str(initID).split('-'))

                        time = str(self.request.POST.get('FAuthvalidity'))

                        #result = get_interface_result(initID, [personID, time])['result']
                        result = 1

                        if result != 1:
                            break

        return  result















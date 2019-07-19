from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from area.models import area
from .models import personauth as T_PersonAuth
from basedata.models import base
from common.views import *
from django.http import JsonResponse
#from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist


def add(request):

    fid = ''.join(str(request.GET.get('fid')).split('-'))

    area_info = area.objects.all()
    areadict = get_dict_transfer(area_info, 'FID', 'FName', 'FStatus')

    auth_info = T_PersonAuth.objects.filter(Q(FPersonID=fid))

    dict_auth = []

    for auth in auth_info:
        dict_auth = dict_auth + [str(auth.FAreaID)]

    authList = json.dumps(dict_auth)

    return render(request, "content/personauth/personauthadd.html", {'resultdict' : areadict, 'authList': authList, 'fid': fid})


def auth(request):
    if request.method == 'POST':
        response_data = {}

        fid = ''.join(str(request.POST.get('fid')).split('-'))
        areaid = request.POST.get('areafid')

        area_info =  json.loads(areaid)

        T_PersonAuth.objects.filter(Q(FPersonID=fid)).delete()

        response_data['result'] = '0'
        for obj in area_info:
            personauth_info = T_PersonAuth()
            personauth_info.FPersonID = fid
            personauth_info.FAreaID = obj['value']
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






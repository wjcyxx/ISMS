from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from device.models import device
from personnel.models import personnel
from pedpassage.models import pedpassage, passagerecord
from django.db.models import Q
from unit.models import unit
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *


class passagedev_callback(View):
    def post(self, request):
        deviceKey = request.POST.get('deviceKey')
        ip = request.POST.get('ip')
        personId = request.POST.get('personId')
        times = request.POST.get('time')
        type = request.POST.get('type')
        
        passageid = get_passageid(deviceKey)
        
        passagerecord_info = passagerecord()
        passagerecord_info.FPersonID_id = personId
        passagerecord_info.FPassageID_id = passageid
        
        if type == 'face_0':
            passagerecord_info.FAuthtypeID = '7f183e98acf411e991437831c1d24216'
        elif type == 'card_0':
            passagerecord_info.FAuthtypeID = '65c7cfb2acf411e991437831c1d24216'
        elif type == 'idcard_0':
            passagerecord_info.FAuthtypeID = '9015ad48acf411e991437831c1d24216'    
            
        personnel_info = personnel.objects.get(Q(FID=personId))
        passagerecord_info.CREATED_PRJ = personnel_info.CREATED_PRJ
        passagerecord_info.CREATED_ORG = personnel_info.CREATED_ORG
        passagerecord_info.CREATED_BY = 'DEV'
        passagerecord_info.UPDATED_BY = 'DEV'
        passagerecord_info.CREATED_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(times)))
            
        passagerecord_info.save()
        
        response_data = {'result': 1, 'success': True}
        
        return HttpResponse(json.dumps(response_data))
        


def get_passageid(devid):
    try:
        device_fid = device.objects.get(Q(FDevID=devid)).FID
        device_fid = ''.join(str(device_fid).split('-'))
        
        pedpassage_fid = pedpassage.objects.filter(Q(FDevID=device_fid)).first().FID
        pedpassage_fid = ''.join(str(pedpassage_fid).split('-'))
        return pedpassage_fid
        
    except ObjectDoesNotExist:
        return None
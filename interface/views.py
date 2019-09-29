from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from device.models import device
from personnel.models import personnel
from pedpassage.models import pedpassage, passagerecord
from devinterface.models import devinterface, interfaceparam
from django.db.models import Q
from unit.models import unit
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import time
import datetime

#人脸一体机识别回调
class passagedev_callback(View):
    def post(self, request):
        deviceKey = request.GET.get('deviceKey')
        ip = request.GET.get('ip')
        personId = request.GET.get('personId')
        times = request.GET.get('time')
        type = request.GET.get('type')
        
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
        passagerecord_info.CREATED_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(times)/1000))
            
        passagerecord_info.save()
        
        response_data = {'result': 1, 'success': True}
        
        return HttpResponse(json.dumps(response_data))

#根据设备ID取通道FID
def get_passageid(devid):
    try:
        device_fid = device.objects.get(Q(FDevID=devid)).FID
        device_fid = ''.join(str(device_fid).split('-'))
        
        pedpassage_fid = pedpassage.objects.filter(Q(FDevID=device_fid)).first().FID
        pedpassage_fid = ''.join(str(pedpassage_fid).split('-'))
        return pedpassage_fid
        
    except ObjectDoesNotExist:
        return None

#根据区域取通道设备及设备接口数据集
def areaid_2_device(areaid):
    pedpassage_info = pedpassage.objects.filter(Q(FAreaID=areaid))

    obj_arr = []

    for obj in pedpassage_info:
        dict = {}

        dict['FDevID'] = obj.FDevID
        dict['FPassageID'] = obj.FID

        devinterface_info = devinterface.objects.filter(Q(FDevID=obj.FDevID)).first()
        dict['FInterID'] = devinterface_info.FID
        dict['FExtID'] = devinterface_info.FInterfaceExtID

        obj_arr.append(dict)

    return obj_arr

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from device.models import device
from personnel.models import personnel
from pedpassage.models import pedpassage, passagerecord
from vehiclefiles.models import vehiclefiles
from vehiclepasslog.models import vehiclepasslog
from vehiclegate.models import vehiclegate
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
from django.conf import settings
import time
import datetime
import os, base64

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

        devinterface_info = devinterface.objects.filter(Q(FDevID=obj.FDevID))

        for obj_interface in devinterface_info:
            dict = {}

            dict['FDevID'] = obj.FDevID
            dict['FPassageID'] = obj.FID

            dict['FInterID'] = obj_interface.FID
            dict['FInterName'] = obj_interface.FName
            dict['FExtID'] = obj_interface.FInterfaceExtID

            obj_arr.append(dict)

    return obj_arr


#车牌识别回调
class vehicleplate_callback(View):
    def post(self, request):

        type = request.POST.get('type')

        if type == 'heartbeat':
            response_data = {'error_num': 0, 'error_str': 'success'}
            return HttpResponse(json.dumps(response_data))

        times = request.POST.get('start_time')
        vehgateID = get_vehiclegateID(request.POST.get('cam_id'))

        vehiclepasslog_info = vehiclepasslog()
        vehiclepasslog_info.FGateID = vehgateID
        vehiclepasslog_info.FPlate = request.POST.get('plate_num')

        if base64_savepic(request.POST.get('picture')):
            vehiclepasslog_info.FPicturepath = 'Plate/'+request.POST.get('plate_num')+'.jpg'

        #vehiclefiles_info = vehiclefiles.objects.get(Q(FPlate=request.POST.get('plate_num')))
        vehiclegate_info = vehiclegate.objects.filter(Q(FID=vehgateID)).first()

        vehiclepasslog_info.CREATED_PRJ = vehiclegate_info.CREATED_PRJ
        vehiclepasslog_info.CREATED_ORG = vehiclegate_info.CREATED_ORG
        vehiclepasslog_info.CREATED_BY = 'DEV'
        vehiclepasslog_info.UPDATED_BY = 'DEV'
        vehiclepasslog_info.CREATED_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(times) / 1000))

        vehiclepasslog_info.save()

        response_data = {'error_num': 0, 'error_str': 'success'}
        return HttpResponse(json.dumps(response_data))


#根据车牌识别ID取通道FID
def get_vehiclegateID(devid):
    device_fid = device.objects.get(Q(FDevID=devid)).FID
    device_fid = ''.join(str(device_fid).split('-'))

    vehiclegate_fid = vehiclegate.objects.filter(Q(FDevID=device_fid)).first().FID
    vehiclegate_fid = ''.join(str(vehiclegate_fid).split('-'))

    return vehiclegate_fid


#根据base64保存图片
def base64_savepic(strBase64, filename):
    save_path = settings.MEDIA_ROOT
    # strBase64 = request.POST.get('strBase64')
    # cfilename = request.POST.get('filename')

    strBase64 =  str(strBase64).replace('-', '+').replace('_', '/').replace('.', '=')

    try:
        with open(save_path+'/'+filename+'.jpg', 'wb') as f:
             f.write(base64.b64decode(strBase64))

        return True
    except Exception as e:
        return False


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

#人脸档案回调
class personcreate_callback(View):
    def post(self, request):
        try:
            personGuid = request.POST.get('personGuid')
            deviceKey = request.POST.get('deviceKey')
            name = request.POST.get('name')
            personFace = request.POST.get('personFace')
            idCard = request.POST.get('idCard')
            sex = request.POST.get('sex')
            birthday = request.POST.get('birthday')
            address = request.POST.get('address')
            nation = request.POST.get('nation')

            devInfo = get_passageid(deviceKey)
            prj_ID = devInfo.CREATED_PRJ

            personnel_info = personnel()
            personnel_info.FPhoto = personGuid
            personnel_info.CREATED_PRJ = prj_ID
            personnel_info.FName = name
            personnel_info.FWoTuFaceGUID = personFace
            personnel_info.FIDcard = idCard
            personnel_info.FHomeaddress = address
            personnel_info.FNation = nation
            if sex == '男':
                personnel_info.FSex = 0
            elif sex == '女':
                personnel_info.FSex = 1

            personnel_info.FBirthday = birthday
            personnel_info.CREATED_ORG = devInfo.CREATED_ORG
            personnel_info.CREATED_BY = 'DEV'
            personnel_info.UPDATED_BY = 'DEV'
            personnel_info.CREATED_TIME = timezone.now()

            personnel_info.save()

            response_data = {'result': 200, 'msg': 'success'}

            return HttpResponse(json.dumps(response_data))

        except Exception as e:
            response_data = {'result': 100, 'msg': 'error:'+str(e)}

            return HttpResponse(json.dumps(response_data))


#人脸一体机识别回调
class passagedev_callback(View):
    def post(self, request):
        try:
            personId = request.POST.get('personGuid')
            deviceKey = request.POST.get('deviceKey')
            picturepath = request.POST.get('photoUrl')
            datatime = request.POST.get('showTime')
            rectype = request.POST.get('type')
            recmode = request.POST.get('recMode')
            temperature = request.POST.get('temperature')

            passageid = get_passageid(deviceKey).FID
            passageid = ''.join(str(passageid).split('-'))

            passagerecord_info = passagerecord()
            passagerecord_info.FPersonID_id = get_personid(personId)
            passagerecord_info.FPassageID_id = passageid
            passagerecord_info.FDeviceID = deviceKey
            passagerecord_info.FType = rectype
            passagerecord_info.FPictureUrl = picturepath
            passagerecord_info.FTemperature = temperature
            passagerecord_info.FPersonGUID = personId

            if recmode == '1':   #刷脸
                passagerecord_info.FAuthtypeID = '7f183e98acf411e991437831c1d24216'
            elif recmode == '2':    #ic卡
                passagerecord_info.FAuthtypeID = '65c7cfb2acf411e991437831c1d24216'
            elif recmode == '3':    #身份证
                passagerecord_info.FAuthtypeID = '9015ad48acf411e991437831c1d24216'

            if get_personid(personId) !=  None:
                personnel_info = personnel.objects.get(Q(FID=personId))
                passagerecord_info.CREATED_PRJ = personnel_info.CREATED_PRJ
                passagerecord_info.CREATED_ORG = personnel_info.CREATED_ORG

            passagerecord_info.CREATED_BY = 'DEV'
            passagerecord_info.UPDATED_BY = 'DEV'
            passagerecord_info.CREATED_TIME = datatime

            passagerecord_info.save()

            response_data = {'result': 200, 'msg': 'success'}

            return HttpResponse(json.dumps(response_data))
        except Exception as e:
            response_data = {'result': 100, 'msg': 'error:'+str(e)}

            return HttpResponse(json.dumps(response_data))


#根据设备ID取通道
def get_passageid(devid):
    try:
        device_fid = device.objects.get(Q(FDevID=devid)).FID
        device_fid = ''.join(str(device_fid).split('-'))
        
        pedpassage_info = pedpassage.objects.filter(Q(FDevID=device_fid)).first()
        return pedpassage_info
        
    except ObjectDoesNotExist:
        return None

#根据人员ID查询人员表并返回结果
def get_personid(personId):
    try:
        personnel.objects.get(Q(FID=personId))
        return personId
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
        devID = request.POST.get('cam_id')

        vehgateID = get_vehiclegateID(devID)

        vehiclepasslog_info = vehiclepasslog()
        vehiclepasslog_info.FGateID_id = vehgateID
        vehiclepasslog_info.FPlate = request.POST.get('plate_num')

        vehicle_pic = request.POST.get('picture')

        timestrip = millis = int(round(time.time()))
        filenames = vehiclepasslog_info.FPlate+'_'+str(timestrip)

        if base64_savepic(vehicle_pic, filenames):
            vehiclepasslog_info.FPicturepath = 'Plate/'+filenames+'.jpg'

        #vehiclefiles_info = vehiclefiles.objects.get(Q(FPlate=request.POST.get('plate_num')))
        vehiclegate_info = vehiclegate.objects.filter(Q(FID=vehgateID)).first()

        vehiclepasslog_info.CREATED_PRJ = vehiclegate_info.CREATED_PRJ
        vehiclepasslog_info.CREATED_ORG = vehiclegate_info.CREATED_ORG
        vehiclepasslog_info.CREATED_BY = 'DEV'
        vehiclepasslog_info.UPDATED_BY = 'DEV'
        vehiclepasslog_info.CREATED_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(times)))

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
        with open(save_path+'/Plate/'+filename+'.jpg', 'wb') as f:
             f.write(base64.b64decode(strBase64))

        return True
    except Exception as e:
        return False


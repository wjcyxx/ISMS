from django.test import TestCase
from django.shortcuts import redirect
from django.db.models import Q
from device.models import device
from basedata.models import base
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os, signal
from threading import Thread
import inspect
import ctypes
import socket
from devinterface.models import devinterface
from device.models import device, devcallinterface
from menchanical.models import menchanical, mecoperauth
from devinterfacesrv.models import envinterfacesrv
from personnel.models import personnel
from baseframe.baseframe import *
from devinterface.models import subinterface
import datetime

# Create your tests here.

def runservice(request):
    SERVICE_NAME = 'EnvdetectionJiandaHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval
    IPADDRESS = devinterface_info.FAddress
    PORT = devinterface_info.FPort


    try:
        print("start...")
        fid = ''.join(str(devinterface_info.FID).split('-'))

        print("主ID:"+fid)
        subinterface_info = subinterface.objects.filter(Q(FPID=fid))

        for subint in subinterface_info:
            interID = ''.join(str(subint.FInterfaceID).split('-'))

            devID = intID_2_devID(interID)

            print("接口ID:"+interID)
            print("设备ID:"+devID)

            result = get_interface_result(interID, [], [], [])

            EnvHisData = envinterfacesrv()
            EnvHisData.FCommandType = 2
            EnvHisData.FDeviceId = devID
            EnvHisData.FSRCTimestamp = time.time()
            EnvHisData.FTimestamp = timezone.now()
            EnvHisData.FSPM = None
            EnvHisData.FNoiseMax = None
            EnvHisData.FTYPE = 2

            prjID = deviceID_2_prjID(devID)
            prj_info = project.objects.get(Q(FID=prjID))

            EnvHisData.FLongitude = prj_info.FLong
            EnvHisData.FLatitude = prj_info.FLat
            EnvHisData.FPressure = None
            EnvHisData.CREATED_PRJ = prjID
            EnvHisData.CREATED_ORG = prj_2_manageorg(prjID)
            EnvHisData.CREATED_BY = 'www.0531yun.cn'
            EnvHisData.UPDATED_BY = 'www.0531yun.cn'
            EnvHisData.CREATED_TIME = timezone.now()

            for env_info in result:
                if env_info['DevAddr'] == devID:

                    if env_info['DevName'] == 'PM':
                        EnvHisData.FPM25 = env_info['DevHumiValue']
                        EnvHisData.FPM10 = env_info['DevTempValue']

                    if env_info['DevName'] == '噪声':
                        EnvHisData.FNoise = env_info['DevHumiValue']

                    if env_info['DevName'] == '温度湿度':
                        EnvHisData.FTemperature = env_info['DevTempValue']
                        EnvHisData.FHumidity = env_info['DevHumiValue']

                    if env_info['DevName'] == '风力风速':
                        EnvHisData.FWIND_SPEED = env_info['DevHumiValue']

                    if env_info['DevName'] == '风向(方位)':
                        EnvHisData.FWIND_DIRECT_STR = env_info['DevTempValue']

                    if env_info['DevName'] == '风向(度数)':
                        EnvHisData.FWIND_DIRECT = env_info['DevHumiValue']

            EnvHisData.save()
            print('本次数据传输完毕')

    except Exception as e:
        pass

def hosit_box_id_2_mecID(box_id):
    dict = {}
    try:
        device_info = device.objects.get(Q(FDevID=box_id))
        dev_fid = ''.join(str(device_info.FID).split('-'))

        mench_info = menchanical.objects.get(Q(FMonitordevID=dev_fid))
        mench_fid = ''.join(str(mench_info.FID).split('-'))
        mench_oper = mecoperauth.objects.filter(Q(FPID=mench_fid)).first()
        personel_info = personnel.objects.get(Q(FID=mench_oper.FAuthpersonID))


        dict['mench_fid'] = mench_fid
        dict['elevator_manager'] = mench_info.FMecmanager
        dict['elevator_mgrtel'] = mench_info.FMecmanagertel
        dict['elevator_oper'] = personel_info.FName
        dict['elevator_opertel'] = personel_info.FTel

        return dict
    except ObjectDoesNotExist:
        return dict

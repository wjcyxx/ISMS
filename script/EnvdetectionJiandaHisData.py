import sys
import os
import django
import socket
import json
import threading
import logging
from django.shortcuts import HttpResponse
import time
import datetime

BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISMS.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q
from common.views import *
from devinterface.models import devinterface
from devinterface.models import subinterface
from device.models import device, devcallinterface
from menchanical.models import menchanical, mecoperauth
from devinterfacesrv.models import envinterfacesrv
from project.models import project
from baseframe.baseframe import *
from devinterfacesrv.models import elevatorinterfacesrv
from django.core.exceptions import ObjectDoesNotExist

if __name__ == "__main__":
    SERVICE_NAME = 'EnvdetectionJiandaHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval
    IPADDRESS = devinterface_info.FAddress
    PORT = devinterface_info.FPort

    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename=SERVICE_NAME+'.log',
                        filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                        )

    def getData():
        try:
            print("start...")
            fid = ''.join(str(devinterface_info.FID).split('-'))

            print("主ID:"+fid)
            subinterface_info = subinterface.objects.filter(Q(FPID=fid))

            for subint in subinterface_info:
                interID = ''.join(str(subint.FInterfaceID).split('-'))

                devID = intID_2_devID(interID)

                logging.info('传输接口ID:' + interID)
                print("接口ID:"+interID)
                print("设备ID:"+devID)

                result = get_interface_result(interID, [], [], [])

                EnvHisData = envinterfacesrv()
                EnvHisData.FCommandType = 2
                #EnvHisData.FDeviceId = devID
                EnvHisData.FSRCTimestamp = time.time()
                EnvHisData.FTimestamp = timezone.now()
                EnvHisData.FSPM = None
                EnvHisData.FPM25 = result[0]['DevHumiValue']
                EnvHisData.FPM10 = result[0]['DevTempValue']
                EnvHisData.FTYPE = 2
                EnvHisData.FWIND_SPEED = result[3]['DevHumiValue']
                EnvHisData.FWIND_DIRECT = result[5]['DevHumiValue']
                EnvHisData.FWIND_DIRECT_STR = result[4]['DevTempValue']
                EnvHisData.FTemperature = result[2]['DevTempValue']
                EnvHisData.FHumidity = result[2]['DevHumiValue']
                EnvHisData.FNoise = result[1]['DevHumiValue']
                EnvHisData.FNoiseMax = None

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

                EnvHisData.save()

                logging.info('本次数据传输完毕, 传输接口为:'+subint.FDesc+', 传输内容: 设备编号：'+ devID +'; PM2.5:'+result[0]['DevHumiValue']+'; PM10:'+result[0]['DevTempValue'])
                print('本次数据传输完毕')

        except Exception as e:
            logging.warning('接口调用失败:'+ str(e))


    def runservice():
        try:
            prjID = devinterface_info.CREATED_PRJ
            prj_info = project.objects.get(Q(FID=prjID))

            logging.info(devinterface_info.FName +':项目扬尘数据服务启动')

            t = threading.Thread(target=getData, args=())
            t.start()
            t.join()

            return True
        except Exception as e:
            return False


    if devinterface_info.FTransmode == 2:           #单次

        if runservice() == False:
            devinterface_info.FSrvStatus = False
            devinterface_info.save()
    elif devinterface_info.FTransmode == 1:         #间隔
        while True:
            if runservice():
                time.sleep(TIME_INTERVAL)
            else:
                devinterface_info.FSrvStatus = False
                devinterface_info.save()

                break


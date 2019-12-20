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
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISMS.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q
from common.views import *
from devinterface.models import devinterface
from device.models import device, devcallinterface
from devinterfacesrv.models import envinterfacesrv, interfacesrvdata
from appkey.models import appkey
from project.models import project
from baseframe.baseframe import *
from devinterfacesrv.models import elevatorinterfacesrv
from django.core.exceptions import ObjectDoesNotExist

if __name__ == "__main__":
    SERVICE_NAME = 'GetWoTuToken'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    interID = ''.join(str(devinterface_info.FID).split('-'))

    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval
    IPADDRESS = devinterface_info.FAddress
    PORT = devinterface_info.FPort
    APPFID = devinterface_info.FAppFID

    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename='GetWoTuToken.log',
                        filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                        )

    def getData():
        try:
            print("start...")
            app_info = appkey.objects.get(Q(FID=APPFID))

            APPID = app_info.FAppID
            APPKEY = app_info.FAppkey
            APPSECRET = app_info.FAppSecret
            TIMESTAMP = round(app_info.FAppCreateTime.timestamp() * 1000)

            strkey = APPKEY+str(TIMESTAMP)+APPSECRET
            md_5 = hashlib.md5()
            md_5.update(strkey.encode("utf-8"))
            SIGN = md_5.hexdigest()

            token = get_interface_result(interID, [APPID, APPKEY, str(TIMESTAMP), SIGN], [], [APPID])['data']
            logging.info('TOKEN:'+token)

            CALL_SIGN_CODE = 'WOTU_APP'
            TAG = 'TOKEN'

            interfacesrvdata_info = interfacesrvdata.objects.filter(Q(FCallSigCode=CALL_SIGN_CODE), Q(FTag=TAG)).first()
            if interfacesrvdata_info == None:
                interfacesrvdata_info = interfacesrvdata()
                interfacesrvdata_info.FCallSigCode = CALL_SIGN_CODE
                interfacesrvdata_info.FTag = TAG
                interfacesrvdata_info.FValue = token
                interfacesrvdata_info.CREATED_PRJ = devinterface_info.CREATED_PRJ
                interfacesrvdata_info.CREATED_ORG = devinterface_info.CREATED_ORG
                interfacesrvdata_info.CREATED_BY = 'SRV'
                interfacesrvdata_info.CREATED_TIME = timezone.now()
                interfacesrvdata_info.UPDATED_BY = 'SRV'

                interfacesrvdata_info.save()
            else:
                interfacesrvdata_info.FTag = TAG
                interfacesrvdata_info.FValue = token

                interfacesrvdata_info.save()

            logging.info('token获取成功')
            print("token添加完成")
        except ObjectDoesNotExist:
            logging.warning('找不到对应的APP，请核查')


    def runservice():
        try:
            logging.info('获取WoTu TOKEN服务启动')

            t = threading.Thread(target=getData, args=())
            t.start()
            t.join()

            return True
        except Exception as e:
            return False


    if devinterface_info.FTransmode == 2:

        if runservice() == False:
            devinterface_info.FSrvStatus = False
            devinterface_info.save()
    elif devinterface_info.FTransmode == 1:

        while True:
            if runservice():
                time.sleep(TIME_INTERVAL)
            else:
                devinterface_info.FSrvStatus = False
                devinterface_info.save()

                break

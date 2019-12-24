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
from device.models import device, devcallinterface
from menchanical.models import menchanical, mecoperauth
from devinterfacesrv.models import envinterfacesrv
from project.models import project
from baseframe.baseframe import *
from devinterfacesrv.models import elevatorinterfacesrv
from django.core.exceptions import ObjectDoesNotExist

if __name__ == "__main__":
    SERVICE_NAME = 'EnvdetectionMetroHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    interID = ''.join(str(devinterface_info.FID).split('-'))

    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval
    IPADDRESS = devinterface_info.FAddress
    PORT = devinterface_info.FPort

    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename='EnvdetectionMetroHisData.log',
                        filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                        )

    def getData(serverThisClient, ClientInfo):
        recvData = serverThisClient.recv(1024)
        recvData = recvData.hex()
        logging.info('info 接收到数据'+str(recvData)+', 来自:'+ClientInfo[0])

        DeviceID = int(recvData[24:32], 16)
        TimeStamp = int(recvData[32:40], 16)
        SPM = int(recvData[40:48], 16)/10000
        PM25 = int(recvData[48:56], 16)/100
        PM10 = int(recvData[56:64], 16)/100
        TYPE = int(recvData[64:68], 16)
        WIND_SPEED = int(recvData[68:76], 16)/100
        WIND_DIRECT = int(recvData[76:84], 16)/10
        Temperature = int(recvData[84:92], 16)/100
        Humidity = int(recvData[92:100], 16)/10
        Noise = int(recvData[100:108], 16)/10
        NoiseMax = int(recvData[108:116], 16)/10
        Longitude = int(recvData[116:124], 16)/1000000
        Latitude = int(recvData[124:132], 16)/1000000
        Pressure = int(recvData[132:140], 16)

        EnvHisData = envinterfacesrv()

        EnvHisData.FDeviceId = str(DeviceID)
        EnvHisData.FSRCTimestamp = TimeStamp

        timeArray = time.localtime(TimeStamp)
        realTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        EnvHisData.FTimestamp = realTime

        EnvHisData.FSPM = SPM
        EnvHisData.FPM25 = PM25
        EnvHisData.FPM10 = PM10
        EnvHisData.FTYPE = TYPE
        EnvHisData.FWIND_SPEED = WIND_SPEED
        EnvHisData.FWIND_DIRECT = WIND_DIRECT
        EnvHisData.FTemperature = Temperature
        EnvHisData.FHumidity = Humidity
        EnvHisData.FNoise = Noise
        EnvHisData.FNoiseMax = NoiseMax
        EnvHisData.FLongitude = Longitude
        EnvHisData.FLatitude = Latitude
        EnvHisData.FPressure = Pressure
        prjID = deviceID_2_prjID(DeviceID)
        EnvHisData.CREATED_PRJ = prjID
        EnvHisData.CREATED_ORG = prjID_2_manorgID(prjID)
        EnvHisData.CREATED_BY = ClientInfo[0]
        EnvHisData.CREATED_TIME = timezone.now()
        EnvHisData.UPDATED_BY = ClientInfo[0]

        EnvHisData.save()

        logging.info('info 本次连接关闭...')
        serverThisClient.close()

    def runservice():
        try:
            Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            Server.bind((IPADDRESS, PORT))
            Server.listen(100)

            logging.info('info TCP/IP 服务启动，开始监听...')
            print('Waiting connect......')

            while True:
                serverThisClient, ClientInfo = Server.accept()
                logging.info('info 等待连接...')
                print('Waiting connect......')

                t = threading.Thread(target=getData, args=(serverThisClient, ClientInfo))
                t.start()
                t.join()

        except Exception as e:
            return False


    def prjID_2_manorgID(prjID):
        try:
            if prjID == '':
                return ''
            else:
                prj_info = project.objects.get(Q(FID=prjID))
            return  prj_info.FManageORG
        except ObjectDoesNotExist:
            return ''

    if devinterface_info.FTransmode != 2:
        if runservice() == False:
            devinterface_info.FSrvStatus = False
            devinterface_info.save()

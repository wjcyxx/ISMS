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
    SERVICE_NAME = 'EnvdetectionHJ2017HisData'

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
        try:
            recvData = serverThisClient.recv(1024)
            recvData = recvData.decode()
            logging.info('info 接收到数据'+str(recvData)+', 来自:'+ClientInfo[0])

            strindex = str(recvData).find('CP')
            lenstr = len(str(recvData))

            # 取头部区域
            headerArea = str(recvData)[0:strindex - 1]
            # 取数据区域
            dataArea = str(recvData)[strindex:lenstr]

            # 序列化头部区域
            headSerialize = headerArea.split(';')

            lstPrex = indexstr(dataArea, '&&')
            dataArea = dataArea[lstPrex[0] + 2:lstPrex[1]]

            # 序列化数据区域
            dataSerialize = dataArea.split(';')

            MN = headSerialize[4]
            len_MN = len(MN)

            # 设备ID
            devID = str(MN)[3:len_MN]

            arr_dts = []
            for dts in dataSerialize:
                arr = []
                _dts = dts.split(',')

                for jdata in _dts:
                    dict = {}

                    _jdata = jdata.split('=')
                    dict['key'] = _jdata[0]
                    dict['value'] = _jdata[1]

                    arr.append(dict)

                arr_dts.append(arr)

            # 数据传入时间

            for i in range(len(arr_dts)):
                keys = arr_dts[i][0]

                if keys['key'] == 'DataTime':  # 数据传入时间
                    src_dataTime = keys['value']
                elif keys['key'] == 'a01001-Cou':  # 温度
                    Temperature = keys['value']
                elif keys['key'] == 'a01002-Cou':  # 湿度
                    Humidity = keys['value']
                elif keys['key'] == 'a01006-Cou':  # 气压
                    Pressure = keys['value']
                elif keys['key'] == 'a01007-Cou':  # 风速
                    Wind_Speed = keys['value']
                elif keys['key'] == 'a01008-Cou':  # 风向
                    Wind_Direct = keys['value']
                elif keys['key'] == 'a34001-Cou':  # TSP
                    TSP = keys['value']

            EnvHisData = envinterfacesrv()

            EnvHisData.FDeviceId = devID
            EnvHisData.FTSP = TSP
            EnvHisData.FCommandType = 2
            EnvHisData.FTemperature = Temperature
            EnvHisData.FHumidity = Humidity
            EnvHisData.FPressure = Pressure
            EnvHisData.FWIND_SPEED = Wind_Speed
            EnvHisData.FWIND_DIRECT = Wind_Direct

            prjID = deviceID_2_prjID(devID)
            EnvHisData.CREATED_PRJ = prjID
            EnvHisData.CREATED_ORG = prjID_2_manorgID(prjID)
            EnvHisData.CREATED_BY = ClientInfo[0]
            EnvHisData.CREATED_TIME = timezone.now()
            EnvHisData.UPDATED_BY = ClientInfo[0]

            EnvHisData.save()

            logging.info('info 本次连接关闭...')
            serverThisClient.close()

        except Exception as e:
            logging.warning('数据接收错误:'+str(e))
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
                #t.join()

        except Exception as e:
            return False


    # 查找指定字符串str1包含指定子字符串str2的全部位置，以列表形式返回
    def indexstr(str1, str2):
        lenth2 = len(str2)
        lenth1 = len(str1)
        indexstr2 = []
        i = 0
        while str2 in str1[i:]:
            indextmp = str1.index(str2, i, lenth1)
            indexstr2.append(indextmp)
            i = (indextmp + lenth2)
        return indexstr2


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

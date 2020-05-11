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
import threading

# Create your tests here.

def runservice(request):
    SERVICE_NAME = 'EnvdetectionJiandaHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval
    IPADDRESS = '192.168.3.27'
    PORT = 8089

    try:
        Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        Server.bind((IPADDRESS, PORT))
        Server.listen(100)

        print('Waiting connect......')

        while True:
            serverThisClient, ClientInfo = Server.accept()
            print('Waiting connect......')

            t = threading.Thread(target=getData, args=(serverThisClient, ClientInfo))
            t.start()
            # t.join()

    except Exception as e:
        return False



def getData(serverThisClient, ClientInfo):
    try:
        recvData = serverThisClient.recv(1024)
        recvData = recvData.decode()


        strindex = str(recvData).find('CP')
        lenstr = len(str(recvData))

        #取头部区域
        headerArea = str(recvData)[0:strindex-1]
        #取数据区域
        dataArea = str(recvData)[strindex:lenstr]

        #序列化头部区域
        headSerialize = headerArea.split(';')

        lstPrex = indexstr(dataArea, '&&')
        dataArea = dataArea[lstPrex[0]+2:lstPrex[1]]

        #序列化数据区域
        dataSerialize = dataArea.split(';')

        MN = headSerialize[4]
        len_MN = len(MN)

        #设备ID
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

        #数据传入时间

        for i in range(len(arr_dts)):
            keys = arr_dts[i][0]

            if keys['key'] == 'DataTime':        #数据传入时间
                src_dataTime = keys['value']
            elif keys['key'] == 'a01001-Cou':    #温度
                Temperature = keys['value']
            elif keys['key'] == 'a01002-Cou':    #湿度
                Humidity = keys['value']
            elif keys['key'] == 'a01006-Cou':    #气压
                Pressure = keys['value']
            elif keys['key'] == 'a01007-Cou':    #风速
                Wind_Speed = keys['value']
            elif keys['key'] == 'a01008-Cou':    #风向
                Wind_Direct = keys['value']
            elif keys['key'] == 'a34001-Cou':    #TSP
                TSP = keys['value']

        EnvHisData = envinterfacesrv()

        EnvHisData.FDeviceId = devID
        EnvHisData.FTSP =  TSP
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

        #print(recvData)

    except Exception as e:
        serverThisClient.close()


#查找指定字符串str1包含指定子字符串str2的全部位置，以列表形式返回
def indexstr(str1,str2):
    lenth2=len(str2)
    lenth1=len(str1)
    indexstr2=[]
    i=0
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
        return prj_info.FManageORG
    except ObjectDoesNotExist:
        return ''



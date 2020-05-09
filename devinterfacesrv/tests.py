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
    IPADDRESS = '192.168.3.18'
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

        headSerialize = headerArea.split(';')
        dataSerialize = dataArea.split(';')

        MN = headSerialize[4]
        len_MN = len(MN)

        devID = str(MN)[3:len_MN]

        print(recvData)

    except Exception as e:
        serverThisClient.close()


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

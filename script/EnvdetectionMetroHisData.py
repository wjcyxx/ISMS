import sys
import os
import django
import socket
import json
import threading
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

    def getData(serverThisClient, ClientInfo):
        recvData = serverThisClient.recv(1024)

        #DeviceID = int(recvData[24:32], 16)
        #TimeStamp = int(recvData[32:40], 16)
        #SPM = int(recvData[40:48], 16)/10000
        #PM25 = int(recvData[48:56], 16)/100
        #PM10 = int(recvData[56:64], 16)/100
        #TYPE = int(recvData[64:68], 16)

        jj = str(recvData, encoding='utf-8')

        print(jj)
        #print(str(DeviceID).encode('utf-8'))
        #print(str(TimeStamp).encode('utf-8'))
        #print(str(SPM).encode('utf-8'))

    def runservice():
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
                t.join()

        except Exception as e:
            return False



    if devinterface_info.FTransmode != 2:
        devinterface_info.FSrvStatus = True
        devinterface_info.save()

        if runservice() == False:
            devinterface_info.FSrvStatus = False
            devinterface_info.save()

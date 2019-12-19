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
from devinterfacesrv.models import envinterfacesrv
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

    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename='GetWoTuToken.log',
                        filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                        )

    def getData():





        pass
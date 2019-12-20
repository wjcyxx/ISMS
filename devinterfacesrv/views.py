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
from menchanical.models import menchanical
from baseframe.baseframe import *
import datetime


def runservice(request):
    SERVICE_NAME = 'EnvdetectionMetroHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    interID = ''.join(str(devinterface_info.FID).split('-'))

    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval
    IPADDRESS = devinterface_info.FAddress
    PORT = devinterface_info.FPort

    try:
        Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        Server.bind(('127.0.0.1', 9000))
        Server.listen(100)
        print('Waiting connect......')

        while True:
            serverThisClient, ClientInfo = Server.accept()
            print('Waiting connect......')

            recvData = serverThisClient.recv(1024)

            x = ClientInfo[0]
            aa = recvData.hex()

            print(aa)

    except Exception as e:
        return False


def devservice(request):
    if request.method == "POST":
        fid = request.POST.get('fid')
        interface_info = devinterface.objects.get(Q(FID=fid))

        srvfile = interface_info.FSrvFile

        pyfiles = settings.BASE_DIR + os.sep + 'script' + os.sep + srvfile + '.py'
        pyfiles = str(pyfiles).replace(' ', '\ ')

        p_id = interface_info.FSrvPID

        cmd = "python3 " + pyfiles
        thread = Thread()
        result = {}

        mode = request.POST.get('mode')
        if mode == '1':
            thread.run = lambda: os.system(cmd)
            thread.start()
            #thread.join()
            result['state'] = 200
            result['msg'] = '服务启动成功'

            interface_info.FSrvStatus = True
            interface_info.save()

            return HttpResponse(json.dumps(result))
        elif mode == '2':
            #stop_cmd = "kill " + str(p_id)
            try:
                interface_info.FSrvStatus = False
                interface_info.save()

                a = os.kill(p_id, signal.SIGKILL)

                result['state'] = 200
                result['msg'] = '服务停止成功'
            except Exception as e:
                interface_info.FSrvStatus = False
                interface_info.save()

                result['state'] = 200
                result['msg'] = '服务停止成功'

            return HttpResponse(json.dumps(result))

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

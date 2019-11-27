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
import os
from threading import Thread
import inspect
import ctypes
from devinterface.models import devinterface
from device.models import device, devcallinterface
from menchanical.models import menchanical
from baseframe.baseframe import *
import datetime


def runservice(request):
    SERVICE_NAME = 'ElevatorHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    interID = ''.join(str(devinterface_info.FID).split('-'))
    # PRJ_ID = devinterface_info.CREATED_PRJ
    PRJ_ID = request.session['PrjID']

    elevator_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=PRJ_ID), Q(FMectypeID='fa606fec009311eaab497831c1d24216'))

    arr_devID = []
    for obj_elevator in elevator_info:
        arr_devID.append(obj_elevator.FMonitordevID)

    device_info = device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=PRJ_ID), Q(FID__in=arr_devID))

    token = ''
    resultdict = []
    dev_id = ''

    for obj_device in device_info:
        fid = ''.join(str(obj_device.FID).split('-'))

        if token == '':
            interface_info = devcallinterface.objects.filter(Q(FPID=fid), Q(FCallSigCode='GETTOKEN')).first()
            initID = interface_info.FInterfaceID

            token = get_interface_result(initID)['data']['token']

        if dev_id == '':
            dev_id = obj_device.FDevID + ', '
        else:
            dev_id = dev_id + obj_device.FDevID + ', '

    endTime = datetime.datetime.now()
    delta = datetime.timedelta(seconds=devinterface_info.FInterval)
    startTime = endTime - delta

    endTime = endTime.strftime('%Y%m%d%H%M%S')
    startTime = startTime.strftime('%Y%m%d%H%M%S')

    result_run = get_interface_result(interID, [token, dev_id, startTime, endTime])['data']
    cnt = str(len(result_run))

    xx =1

def devservice(request):
    if request.method == "POST":
        fid = request.POST.get('fid')
        interface_info = devinterface.objects.get(Q(FID=fid))

        srvfile = interface_info.FSrvFile

        pyfiles = settings.BASE_DIR + os.sep + 'script' + os.sep + srvfile + '.py'
        pyfiles = str(pyfiles).replace(' ', '\ ')

        cmd = "python3 " + pyfiles
        thread = Thread()
        result = {}

        mode = request.POST.get('mode')
        if mode == '1':
            thread.run = lambda: os.system(cmd)
            thread.start()
            thread.join()
            result['status'] = 200
            result['msg'] = '服务启动成功'

            #result_dict['ident'] = thread.ident
        elif mode == '2':
            pass
            # tid = int(request.POST.get('tid'))
            # _async_raise(tid, SystemExit)
        #print(str(os.getppid()))

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

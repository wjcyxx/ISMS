import sys
import os
import django
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
from personnel.models import personnel
from baseframe.baseframe import *
from devinterfacesrv.models import elevatorinterfacesrv
from django.core.exceptions import ObjectDoesNotExist

if __name__ == "__main__":
    SERVICE_NAME = 'ElevatorHisData'

    devinterface_info = devinterface.objects.filter(Q(FSrvFile=SERVICE_NAME)).first()
    interID = ''.join(str(devinterface_info.FID).split('-'))

    devinterface_info.FSrvPID = os.getpid()
    devinterface_info.save()

    TIME_INTERVAL = devinterface_info.FInterval

    def runservice():
        try:
            PRJ_ID = devinterface_info.CREATED_PRJ
            ORG_ID = devinterface_info.CREATED_ORG

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
            delta = datetime.timedelta(seconds=TIME_INTERVAL)
            startTime = endTime - delta

            endTime = endTime.strftime('%Y%m%d%H%M%S')
            startTime = startTime.strftime('%Y%m%d%H%M%S')

            result_run = get_interface_result(interID, [token, dev_id, startTime, endTime])['data']

            for obj_Data in result_run:
                ElevatorHisData = elevatorinterfacesrv()

                ElevatorHisData.FElevatorID = hosit_box_id_2_mecID(obj_Data['hoist_box_id'])['mench_fid']
                ElevatorHisData.hoist_box_id = obj_Data['hoist_box_id']
                ElevatorHisData.cage_id = obj_Data['cage_id']
                ElevatorHisData.door_lock_state = obj_Data['door_lock_state']
                ElevatorHisData.driver_identification_state = obj_Data['driver_identification_state']
                ElevatorHisData.height_percentage = obj_Data['height_percentage']
                ElevatorHisData.hoist_system_state = obj_Data['hoist_system_state']

                timeArray = time.localtime(int(obj_Data['hoist_time'])/1000)
                realTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                ElevatorHisData.hoist_time = realTime

                ElevatorHisData.real_time_gradient1 = obj_Data['real_time_gradient1']
                ElevatorHisData.real_time_gradient2 = obj_Data['real_time_gradient2']
                ElevatorHisData.real_time_height = obj_Data['real_time_height']
                ElevatorHisData.real_time_lifting_weight = obj_Data['real_time_lifting_weight']
                ElevatorHisData.real_time_number_of_people = obj_Data['real_time_number_of_people']
                ElevatorHisData.real_time_or_alarm = obj_Data['real_time_or_alarm']
                ElevatorHisData.real_time_speed = obj_Data['real_time_speed']
                ElevatorHisData.real_time_speed_direction = obj_Data['real_time_speed_direction']
                ElevatorHisData.tilt_percentage1 = obj_Data['tilt_percentage1']
                ElevatorHisData.tilt_percentage2 = obj_Data['tilt_percentage2']
                ElevatorHisData.weight_percentage = obj_Data['weight_percentage']
                ElevatorHisData.system_state = obj_Data['system_state']
                ElevatorHisData.wind_speed = obj_Data['wind_speed']
                ElevatorHisData.elevator_manager = hosit_box_id_2_mecID(obj_Data['hoist_box_id'])['elevator_manager']
                ElevatorHisData.elevator_mgrtel = hosit_box_id_2_mecID(obj_Data['hoist_box_id'])['elevator_mgrtel']
                ElevatorHisData.elevator_oper = hosit_box_id_2_mecID(obj_Data['hoist_box_id'])['elevator_oper']
                ElevatorHisData.elevator_opertel = hosit_box_id_2_mecID(obj_Data['hoist_box_id'])['elevator_opertel']
                ElevatorHisData.CREATED_PRJ = PRJ_ID
                ElevatorHisData.CREATED_ORG = ORG_ID
                ElevatorHisData.CREATED_BY = 'SYS_SRV'
                ElevatorHisData.CREATED_TIME = timezone.now()
                ElevatorHisData.UPDATED_BY = 'SYS_SRV'
                ElevatorHisData.UPDATED_TIME = timezone.now()

                ElevatorHisData.save()

            return True
        except Exception as e:
            return False

        # cnt = str(len(result_run))
        # print(cnt)

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


    if devinterface_info.FTransmode == 2:
        devinterface_info.FSrvStatus = True
        devinterface_info.save()

        if runservice() == False:
            devinterface_info.FSrvStatus = False
            devinterface_info.save()
    else:
        devinterface_info.FSrvStatus = True
        devinterface_info.save()

        while True:
            if runservice():
                time.sleep(TIME_INTERVAL)
            else:
                break

    #    time.sleep(5)
    #    #print(os.getpid())

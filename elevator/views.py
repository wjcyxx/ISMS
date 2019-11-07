from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from project.models import project
from personnel.models import personnel
from menchanical.models import menchanical, mecoperauth
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']
        project_info = project.objects.get(Q(FID=prj_id))
        person_info = personnel.objects.filter(Q(FStatus=0), Q(CREATED_PRJ=prj_id), Q(FSpecialequ=True))

        safemanager_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id), Q(FMectypeID='fa606fec009311eaab497831c1d24216')).values('FMecmanager', 'FMecmanagertel').distinct()


        self.template_name = 'content/elevator/elevatorvisual.html'
        self.context['project_info'] = project_info
        self.context['person_info'] = person_info
        self.context['safemanager_info'] = safemanager_info


class get_datasource(View):
    def post(self, request):
        prj_id = request.session['PrjID']

        initID = 'cdc1cf78cf8111e9af1d7831c1d24216'

        token = get_interface_result(initID)['data']['token']
        request.session['mectoken'] = token

        initSubID = 'b49d3f2ed04d11e9b9dd7831c1d24216'
        resultdict = []

        elevator_info = menchanical.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id), Q(FMectypeID='fa606fec009311eaab497831c1d24216'))

        for dt in elevator_info:
            dict = {}

            fid = ''.join(str(dt.FID).split('-'))
            person_fid = mecoperauth.objects.get(Q(FPID=fid))
            elevotor_oper = personnel.objects.get(Q(FID=person_fid.FAuthpersonID))

            dict['hoist_box_id'] = dt.FMecserialID
            result_run = get_interface_result(initSubID, [token, dt.FMecserialID])['data']
            if len(result_run) == 0:
                dict['status'] = 0
                dict['cage_id'] = '--'
                dict['door_lock_state'] = '--'
                dict['driver_identification_state'] = '--'
                dict['height_percentage'] = '--'
                dict['hoist_system_state'] = '--'
                dict['hoist_time'] = '--'
                dict['real_time_gradient1'] = '--'
                dict['real_time_gradient2'] = '--'
                dict['real_time_height'] = '--'
                dict['real_time_lifting_weight'] = 0
                dict['real_time_number_of_people'] = '--'
                dict['real_time_or_alarm'] = '--'
                dict['real_time_speed'] = '--'
                dict['real_time_speed_direction'] = 3
                dict['tilt_percentage1'] = '--'
                dict['tilt_percentage2'] = '--'
                dict['weight_percentage'] = '--'
                dict['elevator_manager'] = '--'
                dict['elevator_mgrtel'] = '--'

            else:
                dict['status'] = 1
                dict['cage_id'] = result_run[0]['cage_id']
                dict['door_lock_state'] = result_run[0]['door_lock_state']
                dict['driver_identification_state'] = result_run[0]['driver_identification_state']
                dict['height_percentage'] = result_run[0]['height_percentage']
                dict['hoist_system_state'] = result_run[0]['hoist_system_state']
                dict['hoist_time'] = result_run[0]['hoist_time']
                dict['real_time_gradient1'] = result_run[0]['real_time_gradient1']
                dict['real_time_gradient2'] = result_run[0]['real_time_gradient2']
                dict['real_time_height'] = result_run[0]['real_time_height']
                dict['real_time_lifting_weight'] = result_run[0]['real_time_lifting_weight']
                dict['real_time_number_of_people'] = result_run[0]['real_time_number_of_people']
                dict['real_time_or_alarm'] = result_run[0]['real_time_or_alarm']
                dict['real_time_speed'] = result_run[0]['real_time_speed']
                dict['real_time_speed_direction'] = result_run[0]['real_time_speed_direction']
                dict['tilt_percentage1'] = result_run[0]['tilt_percentage1']
                dict['tilt_percentage2'] = result_run[0]['tilt_percentage2']
                dict['weight_percentage'] = result_run[0]['weight_percentage']
                dict['system_state'] = result_run[0]['system_state']
                dict['elevator_manager'] = dt.FMecmanager
                dict['elevator_mgrtel'] = dt.FMecmanagertel
                dict['elevator_oper'] = elevotor_oper.FName
                dict['elevator_opertel'] = elevotor_oper.FTel

            resultdict.append(dict)

        return HttpResponse(json.dumps(resultdict))


class get_run_datasource(View):
    def get(self, request):
        box_id = request.GET.get('boxid')

        initID = 'cdc1cf78cf8111e9af1d7831c1d24216'
        token = get_interface_result(initID)['data']['token']

        initID = 'b49d3f2ed04d11e9b9dd7831c1d24216'
        result = get_interface_result(initID, [token, box_id])['data']

        resultdict = {'code':0, 'msg':"", 'count': len(result), 'data': result}
        return JsonResponse(resultdict, safe=False)






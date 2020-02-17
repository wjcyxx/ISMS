from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from common.views import *
from project.models import project
from projectmap.models import projectmap
from basedata.models import base
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        Orgid = self.request.session['UserOrg']

        self.template_name = 'content/mapview/mapview.html'
        project_info = project.objects.filter(Q(FStatus=True))
        condtions = {"FManageORG": Orgid}
        project_info = org_split(project_info, self.request, **condtions)

        self.context['projectinfo'] = project_info


class get_project(View):
    def post(self, request):
        fid = request.POST.get('fid')
        response_data = {}

        try:
            project_info = project.objects.get(Q(FID=fid))
            response_data['FLong'] = project_info.FLong
            response_data['FLat'] = project_info.FLat
            response_data['result'] = 0

        except ObjectDoesNotExist:
            response_data['result'] = 1

        return HttpResponse(json.dumps(response_data))


class show_projectdetail(EntranceView_base):
    def set_view(self, request):
        long = self.request.GET.get('long')
        lat = self.request.GET.get('lat')

        try:
            fid = ''.join(str(project.objects.get(Q(FLong=long), Q(FLat=lat)).FID).split('-'))
            project_info = project.objects.get(Q(FID=fid))
            project_type = base.objects.get(Q(FID=project_info.FPrjtypeID)).FBase

            now_time = datetime.datetime.now()
            sigdate = project_info.FSigbeginDate
            if sigdate != '' and sigdate != None:
                tempdate = str(project_info.FSigbeginDate).split(' - ')
                begin_day =  datetime.datetime.strptime(tempdate[0], '%Y-%m-%d')
                end_day = datetime.datetime.strptime(tempdate[1], '%Y-%m-%d')

                remain_date = end_day - now_time
                remain_date = str(remain_date.days)

                work_day = now_time - begin_day
                work_day = str(work_day.days)
            else:
                remain_date = '-'
                work_day = '-'

            prjmap_info = projectmap.objects.filter(Q(CREATED_PRJ=fid))


            self.template_name = 'content/datacockpit/projectdetail.html'
            self.context['workday'] = work_day
            self.context['remainday'] = remain_date
            self.context['projectinfo'] = project_info
            self.context['projecttype'] = project_type
            self.context['prjmapinfo'] = prjmap_info
        except ObjectDoesNotExist:
            self.template_name = ''





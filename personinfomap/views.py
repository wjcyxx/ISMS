from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q
from personnel.models import personnel
from pedpassage.models import passagerecord
from group.models import group
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
from django.db import connection
# Create your views here.


#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/personinfomap/personinfomap.html'

        #员工、管理人员在册数量
        person_count = personnel.objects.filter(~Q(FType=0), Q(CREATED_PRJ=prj_id)).count()
        manager_count = personnel.objects.filter(Q(FType=0), Q(CREATED_PRJ=prj_id)).count()

        year = timezone.now().year
        month = timezone.now().month
        day = timezone.now().day

        #员工、管理人员考勤数量
        person_record = passagerecord.objects.filter(Q(CREATED_TIME__year=year), Q(CREATED_TIME__month=month), Q(CREATED_TIME__day=day), ~Q(FPassageID__FType=0), Q(CREATED_PRJ=prj_id)).count()
        manager_record = passagerecord.objects.filter(Q(CREATED_TIME__year=year), Q(CREATED_TIME__month=month), Q(CREATED_TIME__day=day), Q(FPassageID__FType=0), Q(CREATED_PRJ=prj_id)).count()

        #员工登记，退场，禁用数量
        dengji_info = personnel.objects.filter(~Q(FType=0), Q(FStatus=0), Q(CREATED_PRJ=prj_id))
        tuichang_info = personnel.objects.filter(~Q(FType=0),Q(FStatus=1), Q(CREATED_PRJ=prj_id))
        jinyong_info = personnel.objects.filter(~Q(FType=0),Q(FStatus=2), Q(CREATED_PRJ=prj_id))

        #通过刷脸，ic卡，身份证考勤数量
        face_count = passagerecord.objects.filter(Q(CREATED_TIME__year=year), Q(CREATED_TIME__month=month), Q(CREATED_TIME__day=day), ~Q(FPassageID__FType=0), Q(FAuthtypeID='7f183e98acf411e991437831c1d24216'), Q(CREATED_PRJ=prj_id)).count()
        iccard_count = passagerecord.objects.filter(Q(CREATED_TIME__year=year), Q(CREATED_TIME__month=month), Q(CREATED_TIME__day=day), ~Q(FPassageID__FType=0), Q(FAuthtypeID='65c7cfb2acf411e991437831c1d24216'), Q(CREATED_PRJ=prj_id)).count()
        sfz_count = passagerecord.objects.filter(Q(CREATED_TIME__year=year), Q(CREATED_TIME__month=month), Q(CREATED_TIME__day=day), ~Q(FPassageID__FType=0), Q(FAuthtypeID='9015ad48acf411e991437831c1d24216'), Q(CREATED_PRJ=prj_id)).count()

        groupname = group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))

        self.context['person_count'] = person_count
        self.context['tuichang_count'] = tuichang_info.count()
        self.context['jinyong_count'] = jinyong_info.count()
        self.context['person_record'] = person_record
        self.context['manager_count'] = manager_count
        self.context['manager_record'] = manager_record
        self.context['dengji_info'] = dengji_info
        self.context['groupname'] = groupname
        self.context['tuichang_info'] =  tuichang_info
        self.context['jinyong_info'] = jinyong_info
        self.context['face_count'] = face_count
        self.context['iccard_count'] = iccard_count
        self.context['sfz_count'] = sfz_count


#班组数据分析
class groupanalyse(View):
    def post(self, request):
        prj_id = request.session['PrjID']

        group_info = group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)).order_by('FGroup')
        group_data = []
        gperson_data = []
        gpcq_data = []

        for arr in group_info:
            group_data.append(arr.FGroup)

            group_fid = ''.join(str(arr.FID).split('-'))

            person_count = personnel.objects.filter(Q(FGroupID=group_fid), Q(CREATED_PRJ=prj_id)).count()
            gperson_data.append(person_count)

            year = timezone.now().year
            month = timezone.now().month
            day = timezone.now().day
            person_record = passagerecord.objects.filter(Q(FPersonID__FGroupID=group_fid), Q(CREATED_TIME__year=year), Q(CREATED_TIME__month=month), Q(CREATED_TIME__day=day), ~Q(FPassageID__FType=0), Q(CREATED_PRJ=prj_id)).count()
            gpcq_data.append(person_record)


        resultdict = {'group': group_data, 'gpcount': gperson_data, 'gprcount': gpcq_data}

        return JsonResponse(resultdict, safe=False)



#出勤/退场数据分析
class attenanalyse(View):
    def post(self, request):
        cur_time = timezone.now().date()
        month_start_end = get_current_month_start_and_end(cur_time)

        cur = connection.cursor()
        sqlstr = "SELECT DATE_FORMAT( dday, '%m-%d' ) AS dt1, count( * ) - 1 AS FCust FROM(SELECT datelist AS dday FROM calendar WHERE datelist BETWEEN '"+ month_start_end[0] +"' AND '"+ month_start_end[1] +"' UNION ALL SELECT DATE_FORMAT(CREATED_TIME, '%Y-%m-%d' ) AS dt FROM T_Personnel WHERE FStatus = 0 AND DATE_FORMAT(CREATED_TIME, '%Y-%m-%d' ) BETWEEN '"+ month_start_end[0] +"' AND '"+ month_start_end[1] +"' ) a GROUP BY dt1"
        cur.execute(sqlstr)

        rows = cur.fetchall()

        response_days = []
        response_value = []
        response_tc = []

        for r in rows:
            response_days.append(r[0])
            response_value.append(r[1])


        cur1 = connection.cursor()
        sqlstr = "SELECT DATE_FORMAT( dday, '%m-%d' ) AS dt1, count( * ) - 1 AS FCust FROM(SELECT datelist AS dday FROM calendar WHERE datelist BETWEEN '"+ month_start_end[0] +"' AND '"+ month_start_end[1] +"' UNION ALL SELECT DATE_FORMAT(CREATED_TIME, '%Y-%m-%d' ) AS dt FROM T_Personnel WHERE FStatus = 1 AND DATE_FORMAT(CREATED_TIME, '%Y-%m-%d' ) BETWEEN '"+ month_start_end[0] +"' AND '"+ month_start_end[1] +"' ) a GROUP BY dt1"
        cur1.execute(sqlstr)

        rows1 = cur1.fetchall()

        for r1 in rows1:
            response_tc.append(r1[1])


        result_dict = {'FDay': response_days, 'FDengji': response_value, 'FTuic': response_tc}

        return JsonResponse(result_dict, safe=False)



from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from .models import safetrain as T_SafeTrain
from .models import safetrainperson as T_SafeTrainPerson
from personnel.models import personnel
from team.models import team
from group.models import group
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/safetrain/safetraininfo.html'
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.quer_set_fieldnames = ['FBase']


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.GET.get("resultdict[FSubject]", '')
        safetrain_info =  T_SafeTrain.objects.filter(Q(CREATED_PRJ=prj_id), Q(FSubject__contains=serinput))

        return safetrain_info


#链接增加模板
class add(add_base):
    def set_view(self, request):
        self.template_name = 'content/safetrain/safetrainadd.html'
        self.objForm = SafeTrainModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.query_set_idfields = ['FTraintypeID']
        self.query_set_valuefields = ['FBase']

        self.context['team'] = 'null'
        self.context['group'] = 'null'
        self.context['worktype'] = 'null'


#链接编辑模板
class edit(edit_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']

        self.template_name = 'content/safetrain/safetrainadd.html'
        self.model = T_SafeTrain
        self.objForm = SafeTrainModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.query_set_idfields = ['FTraintypeID']
        self.query_set_valuefields = ['FBase']

        team_info = get_dict_table(team.objects.filter(Q(FStatus=True),Q(CREATED_PRJ=prj_id)), 'FID', 'FName')
        group_info = get_dict_table(group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)), 'FID', 'FGroup')
        worktype_info = get_dict_table(base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216')), 'FID', 'FBase')

        self.context['team'] = team_info
        self.context['group'] = group_info
        self.context['worktype'] = worktype_info


#处理新增及保存数据
class insert(insert_base):
    def set_view(self, request):
        self.model = T_SafeTrain
        self.objForm = SafeTrainModelForm
        self.query_sets = [
            base.objects.filter(Q(FPID='aa9b1266b11811e9a09c708bcdb9b39a')),
        ]
        self.query_set_idfields = ['FTraintypeID']
        self.query_set_valuefields = ['FBase']


#选择工人页面入口
class selperson(EntranceView_base):
    def set_view(self, request):
        prj_id = self.request.session['PrjID']
        fid = ''.join(str(self.request.GET.get('fid')).split('-'))

        self.template_name = 'content/safetrain/selpersoninfo.html'
        self.query_sets = [
            team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id)),
            base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216')),
            'fid'
        ]
        self.quer_set_fieldnames = ['FName', 'FGroup', 'FBase', fid]


#返回选择工人table数据及查询结果
class get_selperson_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        prj_id = self.request.session['PrjID']
        serinput = self.request.POST.get("resultdict[FName]", '')
        person_info =  personnel.objects.filter(Q(CREATED_PRJ=prj_id), Q(FName__contains=serinput))

        return person_info


#插入选择的工人
class insert_person(View):
    def post(self, request):
        fpid = request.POST.get('fid')
        data = json.loads(request.POST.get('seldata'))
        response_data = {}

        try:
            for obj in data:
                safetrainperson_info = T_SafeTrainPerson()

                safetrainperson_info.FPID = fpid
                safetrainperson_info.FPersonID_id = ''.join(str(obj['FID']).split('-'))
                safetrainperson_info.FIsQualified = True
                safetrainperson_info.CREATED_PRJ = request.session['PrjID']
                safetrainperson_info.CREATED_ORG = request.session['UserOrg']
                safetrainperson_info.CREATED_BY = request.session['UserID']
                safetrainperson_info.UPDATED_BY = request.session['UserID']
                safetrainperson_info.CREATED_TIME = timezone.now()
                safetrainperson_info.save()

                response_data['result'] = '0'

                return HttpResponse(json.dumps(response_data))

        except Exception as e:
            response_data['result'] = e
            return HttpResponse(json.dumps(response_data))


#显示参与培训的工人列表
class get_person_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        self.type = 1

        fpid = self.request.GET.get('fid')
        trainperson_info = T_SafeTrainPerson.objects.filter(Q(FPID=fpid)).values('FPersonID__FName', 'FPersonID__FSex', 'FPersonID__FIDcard', 'FPersonID__FTeamID', 'FPersonID__FGroupID', 'FPersonID__FWorktypeID', 'FIsQualified', 'FScore')

        return  trainperson_info





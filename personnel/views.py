from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import personnel as T_Personnel
from .models import personcertif as T_PersonnelCertificate
from group.models import group
from team.models import team
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
from group.forms import GroupModelForm
from organize.models import organize
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
#班组管理控制器入口
def personnel(request):
    prj_id = request.session['PrjID']

    team_info = team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
    teaminfo = get_dict_table(team_info, 'FID', 'FName')

    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
    worktypeinfo = get_dict_table(worktype_info, 'FID', 'FBase')

    group_info = group.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=prj_id))
    groupinfo = get_dict_table(group_info, 'FID', 'FGroup')

    return render(request, 'content/personnel/personnelinfo.html', locals())


#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FName]", '')

    prj_id = request.session['PrjID']

    Person_info =  T_Personnel.objects.filter(Q(FName__contains=serinput), Q(CREATED_PRJ=prj_id))
    Person_info = org_split(Person_info, request)

    dict = convert_to_dicts(Person_info)
    resultdict = {'code':0, 'msg':"", 'count': Person_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)


#刷新下拉列表框数据
def ref_dropdowndata(obj, request):
    team_info = team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=request.session['PrjID']))
    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))

    obj.fields['FTeamID'].choices = get_dict_object(request, team_info, 'FID', 'FName')
    obj.fields['FWorktypeID'].choices = get_dict_object(request, worktype_info, 'FID', 'FBase')

#链接增加模板
def add(request):
    if request.method == 'GET':
        fgroupid = ''.join(str(request.GET.get('fid')).split('-'))

        obj = PersonModelForm()

        group_info = group.objects.get(Q(FID=fgroupid))
        GroupForm = GroupModelForm(instance=group_info)

        team_info = team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=request.session['PrjID']))
        GroupForm.fields['FTeamID'].choices = get_dict_object(request, team_info, 'FID', 'FName')

        worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
        GroupForm.fields['FWorktypeID'].choices = get_dict_object(request, worktype_info, 'FID', 'FBase')

        certif_info = base.objects.filter(Q(FPID='691fd5e2a90711e9866b7831c1d24216'))
        certifinfo = get_dict_table(certif_info, 'FID', 'FBase')

        ref_dropdowndata(obj, request)
        return render(request, "content/personnel/personneladd.html" , {'obj': obj, 'GroupForm': GroupForm, 'fgroupid': fgroupid, 'certifinfo':certifinfo, 'action': 'insert'})


#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Person_info = T_Personnel.objects.get(Q(FID=fid))
    fgroupid = Person_info.FGroupID
    obj = PersonModelForm(instance=Person_info)

    group_info = group.objects.get(Q(FID=fgroupid))
    GroupForm = GroupModelForm(instance=group_info)


    team_info = team.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=request.session['PrjID']))
    GroupForm.fields['FTeamID'].choices = get_dict_object(request, team_info, 'FID', 'FName')

    worktype_info = base.objects.filter(Q(FPID='2137f046a6a711e9b7367831c1d24216'))
    GroupForm.fields['FWorktypeID'].choices = get_dict_object(request, worktype_info, 'FID', 'FBase')

    certif_info = base.objects.filter(Q(FPID='691fd5e2a90711e9866b7831c1d24216'))
    certifinfo = get_dict_table(certif_info, 'FID', 'FBase')

    photo_path = Person_info.FPhoto

    ref_dropdowndata(obj, request)

    return render(request, "content/personnel/personneladd.html", {'obj': obj, 'fgroupid': fgroupid, 'GroupForm': GroupForm, 'certifinfo': certifinfo, 'photopath': photo_path, 'action': 'update'})


#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        fgroupid = request.GET.get('fgroupid')

        if request.GET.get('actype') == 'insert':
            obj = PersonModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Person_info = T_Personnel.objects.get(FID=fid)
            obj = PersonModelForm(request.POST, instance=Person_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        #ref_dropdowndata(obj, request)

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                if request.GET.get('actype') == 'insert':
                    temp.FStatus = 0
                temp.FGroupID = fgroupid
                temp.FTeamID = request.POST.get('FTeamID')
                temp.FWorktypeID = request.POST.get('FWorktypeID')
                temp.CREATED_PRJ = request.session['PrjID']
                temp.CREATED_ORG = request.session['UserOrg']
                temp.CREATED_BY = request.session['UserID']
                temp.UPDATED_BY = request.session['UserID']
                temp.CREATED_TIME = timezone.now()

                temp.save()
                response_data['result'] = '0'
            else:
                response_data['msg'] = obj.errors
                response_data['result'] = '1'

            return HttpResponse(json.dumps(response_data))

        except Exception as e:
            response_data['msg'] = e
            response_data['result'] = '1'

            return HttpResponse(json.dumps(response_data))

#处理禁用/启用班组
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Person_info = T_Personnel.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Person_info.FStatus = 2
            elif request.GET.get('type') == 'unlock':
                Person_info.FStatus = 0

            Person_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))


#处理退场/返场
def sign(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Person_info = T_Personnel.objects.get(FID=fid)

            if request.GET.get('type') == 'out':
                Person_info.FStatus = 1
                Person_info.FQuitDate = timezone.now()
            elif request.GET.get('type') == 'in':
                Person_info.FStatus = 0
                Person_info.FQuitDate = None

            Person_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))



#刷新下拉列表框数据
def ref_certidropdowndata(obj, request):
    certiftype_info = base.objects.filter(Q(FPID='691fd5e2a90711e9866b7831c1d24216'))
    obj.fields['FCertitypeID'].choices = get_dict_object(request, certiftype_info, 'FID', 'FBase')


#链接上传图片窗口
def show_upload(request):
    obj = PersonnelCertificateModeForm()
    fid = ''.join(str(request.GET.get('fid')).split('-'))

    ref_certidropdowndata(obj, request)

    if request.method == 'POST':
        obj = PersonnelCertificateModeForm(request.POST, request.FILES)
        ref_certidropdowndata(obj, request)

        if obj.is_valid():
            temp = obj.save(commit=False)
            temp.FPID = request.POST.get('FPID')
            temp.CREATED_PRJ = request.session['PrjID']
            temp.CREATED_ORG = request.session['UserOrg']
            temp.CREATED_BY = request.session['UserID']
            temp.UPDATED_BY = request.session['UserID']
            temp.CREATED_TIME = timezone.now()

            temp.save()

            url = '/personnel/show_upload?fid='+request.POST.get('FPID')
            return redirect(url)

    else:
        return render(request, "content/personnel/certificateupload.html", {'obj': obj, 'fid': fid})

#图片明细数据源
def get_certificate(request):

    if request.method == 'GET':
        fpid = ''.join(str(request.GET.get('fid')).split('-'))

        Certificate_info = T_PersonnelCertificate.objects.filter(Q(FPID=fpid))

        dict = convert_to_dicts(Certificate_info)
        resultdict = {'code':0, 'msg':"", 'count': Certificate_info.count(), 'data': dict}

        return  JsonResponse(resultdict, safe=False)



#链接上传入场安全培训窗口
def showTrain_upload(request):
    fid = ''.join(str(request.GET.get('fid')).split('-'))

    obj = PersonModelForm()

    if request.method == 'POST':
        fid = request.POST.get('FPID')
        Person_info = T_Personnel.objects.get(Q(FID=fid))

        if request.POST.get('FIsSafetrain') == 'on':
            Person_info.FIsSafetrain = True
        else:
            Person_info.FIsSafetrain = False

        if request.POST.get('FSafetrainDate') == '':
            Person_info.FSafetrainDate = None
        else:
            Person_info.FSafetrainDate = request.POST.get('FSafetrainDate')

        if Person_info.FSafetrainHour == '':
            Person_info.FSafetrainHour = 0
        else:
            Person_info.FSafetrainHour = request.POST.get('FSafetrainHour')

        Person_info.FEntranceannex = request.FILES.get('FEntranceannex')
        Person_info.save()

        url = '/personnel/showTrain_upload?fid='+request.POST.get('FPID')
        return redirect(url)

    else:
        return render(request, "content/personnel/safetrainupload.html", {'obj': obj, 'fid': fid})


#链接上传人员照片窗口
def showPhoto_upload(request):
    fid = ''.join(str(request.GET.get('fid')).split('-'))

    obj = PersonModelForm()

    if request.method == 'POST':
        fid = request.POST.get('FPID')
        Person_info = T_Personnel.objects.get(Q(FID=fid))

        Person_info.FPhoto = request.FILES.get('FPhoto')
        Person_info.save()

        url = '/personnel/showPhoto_upload?fid='+request.POST.get('FPID')
        return redirect(url)

    else:
        return render(request, "content/personnel/photoupload.html", {'obj': obj, 'fid': fid})



#入场安全培训数据源
def get_safetrain(request):

    if request.method == 'GET':
        fid = ''.join(str(request.GET.get('fid')).split('-'))

        Person_info = T_Personnel.objects.filter(Q(FID=fid))

        dict = convert_to_dicts(Person_info)
        resultdict = {'code':0, 'msg':"", 'count': Person_info.count(), 'data': dict}

        return  JsonResponse(resultdict, safe=False)


#上传数据至沃土平台
def upload_person(request):
    if request.method == 'POST':
        prj_id = request.session['PrjID']

        upload_info = T_Personnel.objects.filter(Q(FWoTuGUID__isnull=True), Q(CREATED_PRJ=prj_id), Q(FStatus=True))

        for rows in upload_info:


            pass

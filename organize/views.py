from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from .models import organize as T_Organize
from .models import orgQualifications as T_OrgQualifications
from basedata.models import base
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.conf import settings

#组织管理控制器入口
def organize(request):
    #传递组织类型字典到前台页面
    setdata_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
    setdata = get_dict_table(setdata_info, 'FID', 'FBase')

    return render(request, 'content/organize/organizeinfo.html', {'setdata': setdata})

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FOrgname]", '')

    Organize_info = T_Organize.objects.filter(Q(FOrgname__contains=serinput))

    dict = convert_to_dicts(Organize_info)
    resultdict = {'code':0, 'msg':"", 'count': Organize_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

#链接增加模板
def add(request):
    obj = OrganizeModelForm()

    Orgtype_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
    obj.fields['FOrgtypeID'].choices = get_dict_object(request, Orgtype_info, 'FID', 'FBase')

    return render(request, "content/organize/organizeadd.html" , {'obj': obj, 'action': 'insert'})

#链接编辑模板
def edit(request):
    fid = request.GET.get('fid')

    Organize_info = T_Organize.objects.get(FID=fid)

    obj = OrganizeModelForm(instance=Organize_info)

    Orgtype_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
    obj.fields['FOrgtypeID'].choices = get_dict_object(request, Orgtype_info, 'FID', 'FBase')

    return render(request, "content/organize/organizeadd.html", {'obj': obj, 'Organize_info': Organize_info, 'action': 'update' })

#处理新增及保存
def insert(request):
    if request.method == 'POST':
        response_data = {}

        if request.GET.get('actype') == 'insert':
            obj = OrganizeModelForm(request.POST)
        elif request.GET.get('actype') == 'update':
            fid = request.POST.get('FID')
            Orgtype_info = T_Organize.objects.get(FID=fid)
            obj = OrganizeModelForm(request.POST, instance=Orgtype_info)
        else:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))


        Orgtype_info = base.objects.filter(Q(FPID='9defe198a17f11e992e7708bcdb9b39a'))
        obj.fields['FOrgtypeID'].choices = get_dict_object(request, Orgtype_info, 'FID', 'FBase')

        try:
            if obj.is_valid():
                temp = obj.save(commit=False)
                temp.FIssplit = True
                temp.FStatus = True
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


#处理禁用/启用组织
def disabled(request):
    response_data = {}
    if request.method == 'POST':
        fid = request.POST.get('fid')

        try:
            Orgtype_info = T_Organize.objects.get(FID=fid)

            if request.GET.get('type') == 'lock':
                Orgtype_info.FStatus = False
            elif request.GET.get('type') == 'unlock':
                Orgtype_info.FStatus = True

            Orgtype_info.save()

            response_data['result'] = '0'
            return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

    else:
        response_data['result'] = '2'
        return HttpResponse(json.dumps(response_data))

#链接上传图片窗口
def show_upload(request):
    obj = OrganizeQualiModeForm()
    fid = ''.join(str(request.GET.get('fid')).split('-'))

    if request.method == 'POST':
        obj = OrganizeQualiModeForm(request.POST, request.FILES)


        if obj.is_valid():
            temp = obj.save(commit=False)
            temp.FPID = request.POST.get('FPID')
            temp.CREATED_ORG = request.session['UserOrg']
            temp.CREATED_BY = request.session['UserID']
            temp.UPDATED_BY = request.session['UserID']
            temp.CREATED_TIME = timezone.now()

            temp.save()
            
            url = '/organize/show_upload?fid='+request.POST.get('FPID')
            return redirect(url)

    else:
        return render(request, "content/organize/orgainizeupload.html", {'obj': obj, 'fid': fid})

#图片明细数据源
def get_quailfications(request):

    if request.method == 'POST':
        fpid = request.GET.get('fid')

        Qualifications_info = T_OrgQualifications.objects.filter(Q(FPID=fpid))

        dict = convert_to_dicts(Qualifications_info)
        resultdict = {'code':0, 'msg':"", 'count': Qualifications_info.count(), 'data': dict}

        return  JsonResponse(resultdict, safe=False)

def delete(request):
    response_data = {}
    if request.method == 'POST':

        fid = request.POST.get('fid')

        try:
            Qualifications_info = T_OrgQualifications.objects.get(Q(FID=fid))

            the_file = settings.BASE_DIR + os.sep +"media" + os.sep + str(Qualifications_info.FFilepath)

            Qualifications_info.delete()

            if os.path.exists(the_file):
                os.remove(the_file)
                response_data['result'] = '0'
            else:
                response_data['result'] = '1'

            return HttpResponse(json.dumps(response_data))

        except Exception as e:

            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))



















from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import projectmap as T_ProjectMap
from basedata.models import base
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os

# Create your views here.

#项目平面图控制器入口
def projectmap(request):
    #传递平面图类型字典到前台页面
    prjmaptype_info = base.objects.filter(Q(FPID='d4b8fe60a51e11e9afad708bcdb9b39a'))
    prjmaptype = get_dict_table(prjmaptype_info, 'FID', 'FBase')

    return render(request, 'content/projectmap/projectmapinfo.html', {'prjmaptype': prjmaptype})

#返回table数据及查询结果
def get_datasource(request):
    serinput = request.POST.get("resultdict[FMapdesc]", '')

    prj_id = request.session['PrjID']

    Prjmap_info =  T_ProjectMap.objects.filter(Q(FMapdesc__contains=serinput), Q(CREATED_PRJ=prj_id))

    dict = convert_to_dicts(Prjmap_info)
    resultdict = {'code':0, 'msg':"", 'count': Prjmap_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)


def ref_dropdowndata(obj, request):
    Prjmaptype_info = base.objects.filter(Q(FPID='d4b8fe60a51e11e9afad708bcdb9b39a'))
    obj.fields['FMaptypeID'].choices = get_dict_object(request, Prjmaptype_info, 'FID', 'FBase')


#链接上传图片窗口
def prjmap_upload(request):
    obj = ProjectMapModelForm()
    #fid = ''.join(str(request.GET.get('fid')).split('-'))

    if request.method == 'POST':
        obj = ProjectMapModelForm(request.POST, request.FILES)

        ref_dropdowndata(obj, request)

        if obj.is_valid():
            temp = obj.save(commit=False)
            temp.FPID = request.POST.get('FPID')
            temp.CREATED_PRJ = request.session['PrjID']
            temp.CREATED_ORG = request.session['UserOrg']
            temp.CREATED_BY = request.session['UserID']
            temp.UPDATED_BY = request.session['UserID']
            temp.CREATED_TIME = timezone.now()

            temp.save()

            url = '/projectmap/prjmap_upload'
            return redirect(url)

    else:
        ref_dropdowndata(obj, request)
        return render(request, "content/projectmap/prjmapupload.html", {'obj': obj})


#删除项目平面图
def delete(request):
    response_data = {}
    if request.method == 'POST':

        fid = request.POST.get('fid')

        try:
            Prjmap_info = T_ProjectMap.objects.get(Q(FID=fid))

            the_file = settings.BASE_DIR + os.sep +"media" + os.sep + str(Prjmap_info.FFilepath)

            Prjmap_info.delete()

            if os.path.exists(the_file):
                os.remove(the_file)
                response_data['result'] = '0'
            else:
                response_data['result'] = '1'

            return HttpResponse(json.dumps(response_data))

        except Exception as e:

            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from project.models import *
from common.views import *
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_chk(request):
    if request.method == "POST":
        UserID = request.POST.get("UserID")
        Userpwd = request.POST.get("Userpwd")

        response_data = {}
        try:
            user_info = User.objects.get(Q(FUserID=UserID))

            if Userpwd != user_info.FUserpwd:
                response_data['result'] = '1'  # 返回密码输入错误
                return HttpResponse(json.dumps(response_data))

            if user_info.FStatus == False:
                response_data['result'] = '3'  # 返回用户被禁用
                return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:
            response_data['result'] = '2'  # 返回用户没有找到
            return HttpResponse(json.dumps(response_data))

        response_data['result'] = '0'  # 返回正常登录
        response_data['orgid'] = user_info.FOrgID

        request.session['UserID'] = UserID
        request.session['Username'] = user_info.FUsername
        request.session['UserOrg'] = user_info.FOrgID
        return HttpResponse(json.dumps(response_data))

    return HttpResponse(request)

def login_showPrj(request):
    if request.method == "GET":
        orgid = request.GET.get('orgid')

        return render(request, "content/login/showproject.html", {'orgid': orgid})

def get_project(request):
    if request.method == "POST":
        orgid = request.GET.get('orgid')

        serinput = request.POST.get("resultdict[FPrjname]", '')

        prj_info = project.objects.filter(Q(FManageORG=orgid), Q(FPrjname__contains=serinput), Q(FStatus=True))
        dict = convert_to_dicts(prj_info)

        resultdict = {'code': 0, 'msg': "", 'count': prj_info.count(), 'data': dict}
        return JsonResponse(resultdict, safe=False)

def login_ok(request):
    if request.method == "GET":
        prjid = request.GET.get('prjid')
        prjid = ''.join(str(prjid).split('-'))

        prj_info = project.objects.get(Q(FID=prjid))
        request.session['PrjID'] = prjid

        return render(request, "main.html", {'prjinfo': prj_info})

def show(request):
    url = request.GET.get('url')
    #return HttpResponse(url)
    return redirect(url)

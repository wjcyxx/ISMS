from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import *
from project.models import *
from organize.models import organize
from basedata.models import base
from personnel.models import personnel
from device.models import device
from common.views import *
import json
import urllib.parse
from busmenu.models import busmenu
import re

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

        Organize_info = organize.objects.get(Q(FID=user_info.FOrgID))
        if Organize_info.FOrgtypeID == '90644de2f94611e980fe7831c1d24216':
            response_data['orgtype'] = 1
        else:
            response_data['orgtype'] = 0

        request.session['UserID'] = UserID
        request.session['Username'] = user_info.FUsername
        request.session['UserOrg'] = user_info.FOrgID
        request.session['OrgIsSplit'] = Organize_info.FIssplit

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

        condtions = {"FManageORG": orgid}
        prj_info = project.objects.filter(Q(FPrjname__contains=serinput), Q(FStatus=True))
        prj_info = org_split(prj_info, request, **condtions)

        dict = convert_to_dicts(prj_info)

        resultdict = {'code': 0, 'msg': "", 'count': prj_info.count(), 'data': dict}
        return JsonResponse(resultdict, safe=False)

def login_ok(request):
    if request.method == "GET":
        orgtype = request.GET.get('orgtype')
        prjid = request.GET.get('prjid')
        prjid = ''.join(str(prjid).split('-'))

        if orgtype == '0':
            #prj_info = project.objects.all()
            prj_info = project.objects.get(Q(FID=prjid))
            request.session['PrjID'] = prjid

            initID = 'b93df570c31c11e982a27831c1d24216'

            url = get_interface_url(initID)
            param = get_interface_param(initID)

            req = url + '?' + param

            response = urllib.request.urlopen(req)
            data = response.read()
            data = data.decode('utf-8')

            result = json.loads(data)
            devkey = ''


            for r in result:
                if r['DevStatus'] == 'true':
                    devkey = r['DevKey']
                    break

            context = {}
            context['prjinfo'] = prj_info
            context['envdevice'] = result
            context['devkey'] = devkey

            busmenu_info = busmenu.objects.filter(Q(FPID__isnull=True), Q(FStatus=True), Q(FMenuPosition=0)).order_by('FSequence')
            context['busmenu_info'] = busmenu_info

            side_busmenu_info = busmenu.objects.filter(Q(FPID__isnull=True) | Q(FPID=''), Q(FStatus=True), Q(FMenuPosition=1)).order_by('FSequence')
            context['side_busmenu_info'] = side_busmenu_info

            return render(request, "main.html", context)
        else:
            context = {}

            busmenu_info = busmenu.objects.filter(Q(FPID__isnull=True) | Q(FPID=''), Q(FStatus=True), Q(FMenuPosition=2)).order_by('FSequence')
            org_cont = organize.objects.all().count()
            prj_count = project.objects.all().count()
            prj_status = base.objects.filter(Q(FPID='22682ae6a3da11e9920c708bcdb9b39a')).order_by('FBaseID')
            arr_status = []

            for obj in prj_status:
                arr_status.append(obj.FBase)

            prj_cost = project.objects.filter(Q(FStatus=True)).annotate(cost=Sum('FPrjcost')).values('cost')
            dev_count = device.objects.all().count()
            person_regcount = personnel.objects.filter(Q(FStatus=0)).count()

            context['busmenu_info'] = busmenu_info
            context['org_count'] = org_cont
            context['prj_count'] = prj_count
            context['prj_status'] = arr_status
            context['person_regcount'] = person_regcount

            if len(prj_cost) == 0:
                context['prj_cost'] = 0
            else:
                context['prj_cost'] = int(prj_cost[0]['cost'])/10000

            context['dev_count'] = dev_count

            return render(request, "content/datacockpit/datacockpit.html", context)

def show(request):
    url = request.GET.get('url')
    #return HttpResponse(url)
    return redirect(url)


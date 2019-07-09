from django.shortcuts import render
from django.shortcuts import HttpResponse
from login.models import *
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge

def user(request):
    return render(request, 'content/user/userinfo.html')


def get_datasource(request):
    serinput = request.POST.get("resultdict[FBase]", '')

    User_info = User.objects.filter(Q(FUserID__contains=serinput))

    dict = convert_to_dicts(User_info)
    resultdict = {'code':0, 'msg':"", 'count': User_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)


def add(request):
    obj = UserModelForm()

    return render(request, "content/user/useradd.html", {'obj': obj})


def edit(request):
    fid = request.GET.get('fid')

    User_info = User.objects.get(FID=fid)
    obj = UserModelForm(instance=User_info)

    return render(request, "content/user/useredit.html")

def insert(request):
    if request.method == 'POST':
        obj = UserModelForm(request.POST)

        response_data = {}

        if obj.is_valid():
            temp = obj.save(commit=False)
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

def update(request):
    if request.method == 'POST':

        response_data = {}
        fid = request.POST.get('FID')

        User_info = User.objects.get(FID=fid)
        obj = UserModelForm(request.POST, instance=User_info)

        if obj.is_valid():
            temp = obj.save(commit=False)
            temp.UPDATED_BY = request.session['UserID']

            temp.save()
            response_data['result'] = '0'
        else:
            response_data['msg'] = obj.errors
            response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))

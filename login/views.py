from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import *
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
        except ObjectDoesNotExist:

            response_data['result'] = '2'  # 返回用户没有找到
            return HttpResponse(json.dumps(response_data))

        response_data['result'] = '0'  # 返回正常登录
        response_data['orgid'] = user_info.FOrgID

        request.session['UserID'] = UserID
        request.session['Username'] = user_info.FUsername
        request.session['UserOrg'] = user_info.FOrgID
        return HttpResponse(json.dumps(response_data))

def login_showPrj(request):

    if request.method == "GET":
        return render(request, "content/login/showproject.html")
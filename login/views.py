from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json


# Create your views here.

def index(request):
    return render(request, 'index.html')



def login_chk(request):
    if request.method == "POST":
        uact = request.POST.get("email")
        upwd = request.POST.get("password")
        id = request.GET.get("id")

        response_data = {}
        try:
            if id == '0':
                user_info = user.objects.get(Q(FEmail=uact), Q(FType=0))
            elif id == '1':
                user_info = user.objects.get(Q(FMobtel=uact), Q(FType=1))
            elif id == '2':
                user_info = user.objects.get(Q(FUseraccount=uact), Q(FType=3))

            if upwd != user_info.FPwd:
                response_data['result'] = '1'  # 返回密码输入错误
                return HttpResponse(json.dumps(response_data))
        except ObjectDoesNotExist:

            response_data['result'] = '2'  # 返回用户没有找到
            return HttpResponse(json.dumps(response_data))

        response_data['result'] = '0'  # 返回正常登录
        request.session['uact'] = uact
        request.session['utag'] = user_info.FUseraccount
        return HttpResponse(json.dumps(response_data))
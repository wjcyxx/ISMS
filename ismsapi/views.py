from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from common.views import *
from common.views import generate_token
from common.views import certify_token
from appkey.models import appkey as T_AppKey
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import time
import datetime
import hashlib
import re


"""
@api {POST} /ismsapi/get_token/ 获取token
@apiGroup TOKEN
@apiDescription 测试地址:
@apiParam {string} apikey 在后天管理系统中添加的APIKEY[必填]
@apiParam {string} md5 APIKEY和固定公钥hm100合起来做MD5[必填]
@apiSampleRequest http://:8081/ismsapi/get_token/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} token 返回内容
@apiSuccess (消息内容) {string} 0 返回token内容
@apiSuccess (消息内容) {string} 1 md5校验失败
@apiSuccess (消息内容) {string} 2 APIKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 3 API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiSuccessExample {json} 成功返回样例：
{"result": "0", "token": "MTU0NzcwMTAxNC40MDA1MjM6ZTAxOGZmZjA4NjU1ZmI2OWM0ZWI0MWVmNzQwMjkxOTRhYTQ3YzlmNA=="}
@apiErrorExample {json} 错误返回样例：
{"result": "1", "token": "md5 VERIFICATION FAILED"}
{"result": "2", "token": "APIKEY serial is UNREGISTERED"}
{"result": "3", "token": "API interface must be submitted by post method"}

"""
class get_token(View):
    def post(self, request):
        response_data = {}

        appkey = request.POST.get('appkey')
        strmd5 = request.POST.get('md5')
        strpubkey = 'hm100'

        if (appkey == None and strmd5 == None):
            reqbody = request.body
            request_json = json.loads(reqbody.decode("utf-8"))
            appkey = request_json['appkey']
            strmd5 = request_json['md5']

        try:
            appkey_info = T_AppKey.objects.get(Q(FAppkey=appkey), Q(FStatus=True))
            strkey = appkey + strpubkey

            md_5 = hashlib.md5()
            md_5.update(strkey.encode("utf8"))

            sign = md_5.hexdigest()

            if strmd5 == sign:
                token = generate_token(appkey)

                response_data['result'] = '0'
                response_data['token'] = token
            else:
                response_data['result'] = '1'
                response_data['token'] = 'md5 VERIFICATION FAILED'

        except ObjectDoesNotExist:
            response_data['result'] = '2'
            response_data['token'] = 'APIKEY serial is UNREGISTERED'

        return HttpResponse(json.dumps(response_data))

    def get(self, request):
        response_data = {}

        response_data['result'] = '3'
        response_data['token'] = 'API interface must be submitted by post method.'

        return HttpResponse(json.dumps(response_data))


class get_project(View):
    def post(self, request):
        response_data = {}

        appkey = request.POST.get('appkey')
        token = request.POST.get('token')

        if (appkey == None and token == None):
            reqbody = request.body
            request_json = json.loads(reqbody.decode("utf-8"))
            ukey = request_json['appkey']
            token = request_json['token']


        try:
            appkey_info = T_AppKey.objects.get(Q(FAppkey=appkey), Q(FStatus=True))

            response_data = certify_token(appkey, token)
            if response_data != '0':
                return HttpResponse(json.dumps(response_data))
            else:
                dict_prj_arr = []




        except ObjectDoesNotExist:
            pass



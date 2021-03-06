from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from common.views import *
from common.views import generate_token
from common.views import certify_token
from appkey.models import appkey as T_AppKey
from project.models import project
from team.models import team
from login.models import User
from group.models import group
from personnel.models import personnel
from organize.models import organize
from basedata.models import base
from pedpassage.models import pedpassage, passagerecord
from devinterfacesrv.models import envinterfacesrv
from interface.models import prjcheck, prjcheckpic
from device.models import device, devcallinterface
from devinterfacesrv.models import elevatorinterfacesrv
from menchanical.models import menchanical
from receaccount.models import materialsaccount, materaccountgoods
from vehiclepasslog.models import vehiclepasslog
from vehiclegate.models import vehiclegate
from login.models import User
from usergroup.models import usergroup
from busmenu.models import busmenu, authmenu
from filefolder.models import filefolder, uploadfiles
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
from .models import tasklist
from teamworker.models import teamworker, teamworkreply
import time
import datetime
import hashlib
import os
import re
from django.conf import settings


#获取token
"""
@api {POST} /ismsapi/get_token/ 获取token
@apiGroup TOKEN
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_token/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} md5 APPKEY和固定公钥hm100合起来做MD5[必填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_token/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} token 返回内容
@apiSuccess (消息内容) {string} 0 返回token内容
@apiSuccess (消息内容) {string} 1 md5校验失败
@apiSuccess (消息内容) {string} 2 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 3 API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiSuccessExample {json} 成功返回样例：
{"result": "0", "token": "MTU0NzcwMTAxNC40MDA1MjM6ZTAxOGZmZjA4NjU1ZmI2OWM0ZWI0MWVmNzQwMjkxOTRhYTQ3YzlmNA=="}
@apiErrorExample {json} 错误返回样例：
{"result": "1", "token": "md5 VERIFICATION FAILED"}
{"result": "2", "token": "APPKEY serial is UNREGISTERED"}
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
            request_json = eval(reqbody.decode())
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


#获取用户列表
"""
@api {POST} /ismsapi/get_userlist/ 获取用户列表
@apiGroup BD
@apiDescription 调用地址:http://121.196.23.69/ismsapi/get_userlist/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} ORGID组织UUID[必填]
@apiSampleRequest http://121.196.23.69/ismsapi/get_userlist/ 
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 消息
@apiSuccess (消息内容) {string} 0 校验正常
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 用户UUID，唯一标识
@apiSuccess (结构体) {string} FUserID 用户账户
@apiSuccess (结构体) {string} FUserpwd 用户密码
@apiSuccess (结构体) {string} FType 用户类型0:企业账户1:合作伙伴2:管理员3:政务平台
@apiSuccess (结构体) {string} FStatus 用户启用状态
@apiSuccess (结构体) {string} FUsername 用户名称
@apiSuccess (结构体) {string} FOrgID 所属组织
@apiSuccess (结构体) {string} FRoleID 用户角色
@apiSuccess (结构体) {string} FTel 联系电话
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiSuccessExample {json} 成功返回样例：
{"result": "0", "msg": "success"}
"""
class get_userlist(api_common):
    def set_view(self, request):
        orgID = self.request.POST.get('ORGID')

        if orgID != None:
            try:
                organize_info = organize.objects.get(Q(FID=orgID))
            except ObjectDoesNotExist:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '组织UUID不存在'

                return

        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '组织UUID不能为空'

            return

        user_info = User.objects.filter(Q(CREATED_ORG=orgID))

        self.response_data['result'] = '0'
        self.response_data['msg'] = 'success'
        self.response_data['data'] = convert_to_dicts(user_info)


# 获取用户组
"""
@api {POST} /ismsapi/get_usergroup/ 获取用户组列表
@apiGroup AUTH
@apiDescription 调用地址:http://121.196.23.69/ismsapi/get_usergroup/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://121.196.23.69/ismsapi/get_usergroup/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 用户组结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 用户组UUID，唯一标识,根据此关键字段进行检索
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FName 用户组名称
@apiSuccess (结构体) {string} FDesc 用户组描述
@apiSuccess (结构体) {string} FStatus 用户组状态
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_usergroup(api_base):
    def set_view(self, request):
        self.model = usergroup


# 获取菜单列表
"""
@api {POST} /ismsapi/get_busmenu/ 获取菜单项列表
@apiGroup AUTH
@apiDescription 调用地址:http://121.196.23.69/ismsapi/get_busmenu/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://121.196.23.69/ismsapi/get_busmenu/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 用户组结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 菜单项UUID，唯一标识,根据此关键字段进行检索
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FPID 菜单项父UUID
@apiSuccess (结构体) {string} FSequence 排序顺序号
@apiSuccess (结构体) {string} FMenuID 菜单项编号
@apiSuccess (结构体) {string} FMenuName 菜单项名称
@apiSuccess (结构体) {string} FStatus 用户组状态
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_busmenu(api_base):
    def set_view(self, request):
        self.model = busmenu


# 新增用户组菜单权限
"""
@api {POST} /ismsapi/add_authmenu/ 新增用户组菜单权限
@apiGroup AUTH
@apiDescription 调用地址:http://121.196.23.69/ismsapi/add_authmenu/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FUserGroupID 用户组UUID[必填]
@apiParam {string} FBusMenuID 菜单项UUID, 多个菜单项之间用逗号分割开[必填]
@apiSampleRequest http://121.196.23.69/ismsapi/add_authmenu/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 用户组结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 权限项UUID，唯一标识,根据此关键字段进行检索
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FUserGroupID 用户组UUID
@apiSuccess (结构体) {string} FBusMenuID 菜单项UUID
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class add_authmenu(api_common):
    def set_view(self, request):
        usergroupID = self.request.POST.get('FUserGroupID')
        busmenuID = self.request.POST.get('FBusMenuID')

        if usergroupID != None:
            try:
                usergroup_info = usergroup.objects.get(Q(FID=usergroupID))
            except ObjectDoesNotExist:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '用户组UUID不存在'

                return
        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '用户组UUID不能为空'

            return

        if busmenuID == None:
            self.response_data['result'] = '12'
            self.response_data['msg'] = '菜单项UUID不能为空'

            return

        busmenu_array = str(busmenuID).split(',')

        data = []
        for _list in busmenu_array:
            try:
                busmenu_info = busmenu.objects.get(Q(FID=_list))

                dict = {}
                authmenu_info = authmenu()
                authmenu_info.FUserGroupID = usergroupID
                authmenu_info.FBusMenuID = _list
                authmenu_info.CREATED_ORG = busmenu_info.CREATED_ORG
                authmenu_info.CREATED_BY = 'API'
                authmenu_info.CREATED_TIME = timezone.now()
                authmenu_info.UPDATED_BY = 'API'

                authmenu_info.save()

                dict['FID'] = authmenu_info.FID
                dict['FID_Split'] = ''.join(str(authmenu_info.FID).split('-'))
                dict['FUserGroupID'] = usergroupID
                dict['FBusMenuID'] = _list
                dict['CREATED_ORG'] = authmenu_info.CREATED_ORG
                dict['CREATED_BY'] = 'API'
                dict['CREATED_TIME'] = authmenu_info.CREATED_TIME

                data.append(dict)

            except ObjectDoesNotExist:
                self.response_data['result'] = '13'
                self.response_data['msg'] = '菜单项目【'+ _list +'】UUID 不存在'

                return


        self.response_data['result'] = '0'
        self.response_data['msg'] = '菜单权限分配成功'
        self.response_data['data'] = data


# 移除菜单项权限
"""
@api {POST} /ismsapi/remove_authmenu/ 移除用户组菜单权限
@apiGroup AUTH
@apiDescription 调用地址:http://121.196.23.69/ismsapi/remove_authmenu/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FUserGroupID 用户组UUID[必填]
@apiParam {string} FBusMenuID 菜单项UUID, 多个菜单项之间用逗号分割开[必填]
@apiSampleRequest http://121.196.23.69/ismsapi/remove_authmenu/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 用户组结构体
@apiSuccess (消息内容) {string} 0 权限移除成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class remove_authmenu(api_common):
    def set_view(self, request):
        usergroupID = self.request.POST.get('FUserGroupID')
        busmenuID = self.request.POST.get('FBusMenuID')

        if usergroupID == None:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '用户组UUID不能为空'

            return

        if busmenuID != None:
            busmenu_array = str(busmenuID).split(',')

            authmenu.objects.filter(Q(FBusMenuID__in=busmenu_array), Q(FUserGroupID=usergroupID)).delete()

            self.response_data['result'] = '0'
            self.response_data['msg'] = '权限项移除成功'

            return
        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '菜单项UUID不能为空'

            return


# 根据用户组获取菜单项权限
"""
@api {POST} /ismsapi/get_authmenu/ 获取用户组菜单权限
@apiGroup AUTH
@apiDescription 调用地址:http://121.196.23.69/ismsapi/get_authmenu/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FUserGroupID 用户组UUID[必填]
@apiSampleRequest http://121.196.23.69/ismsapi/get_authmenu/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 用户组结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 权限项UUID，唯一标识,根据此关键字段进行检索
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FUserGroupID 用户组UUID
@apiSuccess (结构体) {string} FBusMenuID 菜单项UUID
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_authmenu(api_common):
    def set_view(self, request):
        usergroupID = self.request.POST.get('FUserGroupID')

        if usergroupID == None:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '用户组UUID不能为空'

            return

        authmenu_info = authmenu.objects.filter(Q(FUserGroupID=usergroupID))

        self.response_data['result'] = '0'
        self.response_data['msg'] = 'success'
        self.response_data['data'] = convert_to_dicts(authmenu_info)

#获取组织信息
"""
@api {POST} /ismsapi/get_orgainze/ 获取组织信息
@apiGroup BD
@apiDescription 调用地址:http://121.196.23.69/ismsapi/get_orgainze/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} ORGID组织UUID[必填]
@apiSampleRequest http://121.196.23.69/ismsapi/get_orgainze/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 消息
@apiSuccess (消息内容) {string} 0 校验正常
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccessExample {json} 成功返回样例：
{"result": "0", "msg": "success"}
"""
class get_orgainze(api_base):
    def set_view(self, request):
        self.model = organize


#校验用户名是否存在
"""
@api {POST} /ismsapi/check_user/ 检查用户名称是否有效
@apiGroup BD
@apiDescription 调用地址:http://39.106.148.205/ismsapi/check_user/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} user 需要校验的用户名称[必填]
@apiParam {string} password 需要校验的密码[必填]
@apiSampleRequest http://39.106.148.205/ismsapi/check_user/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 消息
@apiSuccess (消息内容) {string} 0 校验正常
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 用户不存在
@apiSuccess (消息内容) {string} 6 用户密码错误
@apiSuccess (消息内容) {string} 7 用户被禁用
@apiSuccessExample {json} 成功返回样例：
{"result": "0", "msg": "此用户正常"}
"""
class check_user(View):
    def post(self, request):
        response_data = {}

        appkey = request.POST.get('appkey')
        token = request.POST.get('token')
        user = request.POST.get('user')
        password = request.POST.get('password')

        if (appkey == None and token == None):
            reqbody = request.body
            request_json = eval(reqbody.decode())
            appkey = request_json['appkey']
            token = request_json['token']
            user = request_json['user']
            password = request_json['password']

        try:
            appkey_info = T_AppKey.objects.get(Q(FAppkey=appkey), Q(FStatus=True))
            response_data = certify_token(appkey, token)

            if response_data['result'] != '0':
                return HttpResponse(json.dumps(response_data))
            else:
                user_info = User.objects.filter(Q(FUserID=user))

                if user_info.count() == 0:
                    response_data['result'] = '5'
                    response_data['msg'] = '此用户不存在'
                else:
                    pwd = user_info[0].FUserpwd
                    if pwd == password:
                        if user_info[0].FStatus == True:
                            response_data['result'] = '0'
                            response_data['msg'] = '此用户正常'
                        else:
                            response_data['result'] = '7'
                            response_data['msg'] = '此用户已被禁用'
                    else:
                        response_data['result'] = '6'
                        response_data['msg'] = '用户密码错误'

            return JsonResponse(response_data, safe=False)

        except ObjectDoesNotExist:
            response_data['result'] = '4'
            response_data['msg'] = 'APIKEY serial is UNREGISTERED'

            return HttpResponse(json.dumps(response_data))



#获取字典数据api接口
"""
@api {POST} /ismsapi/get_basedate/ 获取字典数据列表
@apiGroup BD
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_basedate/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_basedate/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 字典UUID，唯一标识,根据此关键字段进行检索
@apiSuccess (结构体) {string} FPID 字典父类UUID
@apiSuccess (结构体) {string} FBaseID 字典编号
@apiSuccess (结构体) {string} FBase 字典名称
@apiSuccess (结构体) {string} FDesc 字典描述
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_basedate(api_base):
    def set_view(self, request):
        self.model = base


#获取项目列表api接口
"""
@api {POST} /ismsapi/get_project/ 获取项目列表
@apiGroup PROJECT
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_project/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_project/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 项目UUID，项目唯一标识
@apiSuccess (结构体) {string} FPrjID 项目编码
@apiSuccess (结构体) {string} FPrjname 项目名称
@apiSuccess (结构体) {string} FShortname 项目简称
@apiSuccess (结构体) {string} FPrjtypeID 工程类别
@apiSuccess (结构体) {string} FPrjuseID 工程用途
@apiSuccess (结构体) {string} FPrjstate 工程状态
@apiSuccess (结构体) {string} FStructypeID 结构类型ID,需要调用字典接口获取翻译内容
@apiSuccess (结构体) {string} FPrjcost 工程造价
@apiSuccess (结构体) {string} FArea 建筑面积
@apiSuccess (结构体) {string} FAddress 项目地址
@apiSuccess (结构体) {float} FLong 经度
@apiSuccess (结构体) {float} FLat 纬度
@apiSuccess (结构体) {string} FSigDate 合同签订日期
@apiSuccess (结构体) {string} FSigbeginDate 合同工期
@apiSuccess (结构体) {string} FSigendDate 合同截止日期
@apiSuccess (结构体) {string} FBeginDate 实际工期
@apiSuccess (结构体) {string} FEndDate 实际截止日期
@apiSuccess (结构体) {string} FPrjmanager 项目经理
@apiSuccess (结构体) {string} FPrjmanagertel 项目经理电话
@apiSuccess (结构体) {string} FWinOrgID 中标单位
@apiSuccess (结构体) {string} FWinAtten 中标单位联系人
@apiSuccess (结构体) {string} FWinAttenTel 中标单位联系人电话
@apiSuccess (结构体) {string} FBuildOrgID 建设单位
@apiSuccess (结构体) {string} FBuildAtten 建设单位联系人
@apiSuccess (结构体) {string} FBuildAttenTel 建设单位联系人电话
@apiSuccess (结构体) {string} FDesignOrgID 设计单位
@apiSuccess (结构体) {string} FDesignAtten 设计单位联系人
@apiSuccess (结构体) {string} FDesignAttenTel 设计单位联系人电话
@apiSuccess (结构体) {string} FSuperviseOrgID 监理单位
@apiSuccess (结构体) {string} FSuperviseAtten 监理单位联系人
@apiSuccess (结构体) {string} FSuperviseAttenTel 监理单位联系人电话
@apiSuccess (结构体) {string} FUserOrgID 业主单位
@apiSuccess (结构体) {string} FUserAtten 业主单位联系人
@apiSuccess (结构体) {string} FUserAttenTel 业主单位联系人电话
@apiSuccess (结构体) {string} FPrjdesc 工程概况
@apiSuccess (结构体) {boolean} FStatus 状态【True:启用，False:禁用】
@apiSuccess (结构体) {string} FManageORG 管理组织,需要调用组织接口获取翻译
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_project(api_base):
    def set_view(self, request):
        self.model = project


#获取组织列表api接口
"""
@api {POST} /ismsapi/get_orgainze/ 获取组织列表
@apiGroup PROJECT
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_orgainze/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_orgainze/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 组织UUID，唯一标识
@apiSuccess (结构体) {string} FOrgID 统一社会信用代码
@apiSuccess (结构体) {string} FQualevel 主项资质等级
@apiSuccess (结构体) {string} FOrgname 组织名称
@apiSuccess (结构体) {string} FOrgtypeID 组织类型,需要调用字典接口获取翻译内容
@apiSuccess (结构体) {string} provid 所属省份,需要调用区域接口获取翻译内容
@apiSuccess (结构体) {string} cityid 所属城市,需要调用区域接口获取翻译内容
@apiSuccess (结构体) {string} areaid 所属区域,需要调用区域接口获取翻译内容
@apiSuccess (结构体) {string} FOrgaddress 组织地址
@apiSuccess (结构体) {float} FLong 经度
@apiSuccess (结构体) {float} FLat 纬度
@apiSuccess (结构体) {string} FStructypeID 结构类型ID,需要调用字典接口获取翻译内容
@apiSuccess (结构体) {string} FPrjcost 工程造价
@apiSuccess (结构体) {string} FArea 建筑面积
@apiSuccess (结构体) {string} FAddress 项目地址
@apiSuccess (结构体) {string} FLong 经度
@apiSuccess (结构体) {string} FLat 纬度
@apiSuccess (结构体) {string} FLar 法人代表
@apiSuccess (结构体) {string} FLartel 法人代表电话
@apiSuccess (结构体) {string} FLarIDcard 法人代表身份证
@apiSuccess (结构体) {float} FRegcapital 注册资金
@apiSuccess (结构体) {date} FRegDate 注册日期
@apiSuccess (结构体) {string} FLicenceno 安全施工许可证号
@apiSuccess (结构体) {string} FValidDate 许可证有效日期
@apiSuccess (结构体) {string} FLicauthority 发证机关
@apiSuccess (结构体) {string} FHrcharge 劳资负责人姓名
@apiSuccess (结构体) {string} FHrIDcard 劳资负责人身份证
@apiSuccess (结构体) {string} FHrtel 劳资负责人电话
@apiSuccess (结构体) {boolean} FIssplit 是否数据隔离【True:隔离，False:不隔离】
@apiSuccess (结构体) {string} FScope 经营范围
@apiSuccess (结构体) {boolean} FStatus 状态【True:启用，False:禁用】
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_orgainze(api_base):
    def set_view(self, request):
        self.model = organize


#获取施工队列表api接口
"""
@api {POST} /ismsapi/get_team/ 获取施工队列表
@apiGroup HU
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_team/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_team/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 施工队UUID，唯一标识
@apiSuccess (结构体) {string} FOrgID 所属分包商,需要调用组织管理接口获取分包商名称
@apiSuccess (结构体) {string} FName 施工队名称
@apiSuccess (结构体) {string} FTeammgr 施工队项目经理
@apiSuccess (结构体) {string} FMgrtel 联系电话
@apiSuccess (结构体) {string} FIDcard 身份证
@apiSuccess (结构体) {date} FFirstDate 合同签订日期
@apiSuccess (结构体) {string} FScope 承包范围
@apiSuccess (结构体) {float} FAmount 承包金额
@apiSuccess (结构体) {integer} FEvaluate 评价【0:合格,1:不合格】
@apiSuccess (结构体) {string} FAddress 项目地址
@apiSuccess (结构体) {integer} FScale 队伍规模
@apiSuccess (结构体) {string} FSource 队伍来源
@apiSuccess (结构体) {string} FDesc 备注
@apiSuccess (结构体) {boolean} FStatus 状态【True:启用，False:禁用】
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口获取指定项目的施工队
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""

class get_team(api_base):
    def set_view(self, request):
        self.model = team


#获取班组列表api接口
"""
@api {POST} /ismsapi/get_group/ 获取班组列表
@apiGroup HU
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_group/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_group/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 班组UUID，唯一标识
@apiSuccess (结构体) {string} FWorktypeID 班组工种,需要调用字典接口获取翻译内容
@apiSuccess (结构体) {string} FGroup 班组名称
@apiSuccess (结构体) {string} FTeamID 所属施工队,根据施工队过滤班组
@apiSuccess (结构体) {string} FDesc 备注
@apiSuccess (结构体) {boolean} FStatus 状态【True:启用，False:禁用】
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口过滤指定项目的班组
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_group(api_base):
    def set_view(self, request):
        self.model = group


#获取人员列表api接口
"""
@api {POST} /ismsapi/get_personnel/ 获取人员列表
@apiGroup HU
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_personnel/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_personnel/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 人员UUID，唯一标识
@apiSuccess (结构体) {string} FName 人员姓名
@apiSuccess (结构体) {integer} FType 员工类型【0:管理人员,1:班组长,2:员工】
@apiSuccess (结构体) {string} FWorktypeID 所属工种,需要调用字典接口获取翻译内容
@apiSuccess (结构体) {string} FGroupID 所属班组,根据班组过滤人员
@apiSuccess (结构体) {string} FTeamID 所属施工队,根据施工队过滤人员
@apiSuccess (结构体) {boolean} FIsSafetrain 是否进行安全培训【True:是,False:否】
@apiSuccess (结构体) {boolean} FSpecialequ 是否操作特种设备【True:是,False:否】
@apiSuccess (结构体) {date} FSafetrainDate 培训时间
@apiSuccess (结构体) {integer} FSafetrainHour 培训课时
@apiSuccess (结构体) {string} FEntranceannex 进场附件,图片在服务器上存储的路径
@apiSuccess (结构体) {string} FIDcard 身份证号
@apiSuccess (结构体) {date} FIDcardbeginDate 身份证有效起始日期
@apiSuccess (结构体) {date} FIDcardendDate 身份证有效结束日期
@apiSuccess (结构体) {boolean} FIDcardIsIndefinite 身份证长期有效【True:是,False:否】
@apiSuccess (结构体) {integer} FSex 性别【0:男,1:女】
@apiSuccess (结构体) {string} FNation 民族
@apiSuccess (结构体) {date} FBirthday 出生日期
@apiSuccess (结构体) {string} FNaviveplace 籍贯
@apiSuccess (结构体) {string} FHomeaddress 家庭住址
@apiSuccess (结构体) {string} FSignorg 签发机关
@apiSuccess (结构体) {string} FTel 联系方式
@apiSuccess (结构体) {string} FPolitident 政治面貌
@apiSuccess (结构体) {string} FSpeciality 特长
@apiSuccess (结构体) {integer} FMarital 婚姻状况【0:未婚,1:已婚,2:离异】
@apiSuccess (结构体) {string} FLevelofedu 文化程度
@apiSuccess (结构体) {string} FTempaddress 暂住地址
@apiSuccess (结构体) {string} FBank 开户银行
@apiSuccess (结构体) {string} FBankaccount 银行账号
@apiSuccess (结构体) {string} FEmercontact 紧急联系人
@apiSuccess (结构体) {string} FEmercontacttel 紧急联系人电话
@apiSuccess (结构体) {string} FPhoto 照片,照片图片在服务器上存储的路径
@apiSuccess (结构体) {boolean} FContractState 劳动合同【True:签订,False:未签订】
@apiSuccess (结构体) {datetime} FQuitDate 退场日期
@apiSuccess (结构体) {string} FDesc 备注
@apiSuccess (结构体) {integer} FStatus 状态【0:登记,1:退场,2:禁用】
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口过滤指定项目的班组
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_personnel(api_base):
    def set_view(self, request):
        self.model = personnel


#获取通道列表api接口
"""
@api {POST} /ismsapi/get_pedpassage/ 获取人行通道列表
@apiGroup HU
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_pedpassage/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_pedpassage/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 通道UUID，唯一标识
@apiSuccess (结构体) {string} FPassage 通道名称
@apiSuccess (结构体) {string} FDevID 设备编号,对映到具体的闸机设备
@apiSuccess (结构体) {string} FAreaID 区域编号,需要调用项目区域接口翻译内容,表明闸机所在区域
@apiSuccess (结构体) {integer} FType 通道类型【0:入口,1:出口】
@apiSuccess (结构体) {string} FDesc 备注
@apiSuccess (结构体) {boolean} FStatus 状态【True:启用,False:禁用】
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口过滤指定项目的班组
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 创建时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_pedpassage(api_base):
    def set_view(self, request):
        self.model = pedpassage


#获取通道通行记录列表api接口
"""
@api {POST} /ismsapi/get_passagerecord/ 获取通道通行记录列表
@apiGroup HU
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_passagerecord/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_passagerecord/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FPersonID 人员ID
@apiSuccess (结构体) {string} FPassageID 人行通道ID,对映到具体的通道,需要调用通道列表接口获取
@apiSuccess (结构体) {string} FAuthtypeID 通行授权方式,需要调用字典接口获取翻译内容
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口过滤指定项目的班组
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 通行时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_passagerecord(api_base):
    def set_view(self, request):
        self.model = passagerecord



#获取机械设备列表api接口
"""
@api {POST} /ismsapi/get_menchanical/ 获取机械设备列表
@apiGroup DEV
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_menchanical/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {json} conditions 过滤条件,必须为JSON格式,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填]
@apiSampleRequest http://39.106.148.205/ismsapi/get_menchanical/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FMecserialID 机械唯一编码
@apiSuccess (结构体) {string} FMectypeID 机械类型,升降机械:fa606fec009311eaab497831c1d24216,起重机械:f9f44816bd7311e9a59c7831c1d24216,桩工机械:064d7e0cbd7411e9a59c7831c1d24216,压实机械:13e4ecf8bd7411e9a59c7831c1d24216
@apiSuccess (结构体) {string} FMecspec 机械型号
@apiSuccess (结构体) {string} FMecsource 机械来源:0自有,1租赁
@apiSuccess (结构体) {string} FOwnerOrg 产权单位
@apiSuccess (结构体) {string} FRecordNo 产权备案号
@apiSuccess (结构体) {string} FRecorddate 备案日期
@apiSuccess (结构体) {string} FLease 租赁单位
@apiSuccess (结构体) {string} FManufacturer 生产厂家
@apiSuccess (结构体) {string} FProducdate 出厂日期
@apiSuccess (结构体) {string} FProducNo 出厂编号
@apiSuccess (结构体) {string} FMecmanager 机械管理员
@apiSuccess (结构体) {string} FMecmanagertel 联系方式
@apiSuccess (结构体) {string} FParameter 机械参数
@apiSuccess (结构体) {string} FStatus 状态:True启用False禁用
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 通行时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_menchanical(api_base):
    def set_view(self, request):
        self.model = menchanical


#获取升降机监测数据(通用接口)
"""
@api {POST} /ismsapi/get_elevator_hisdata/ 获取升降机监测数据(通用接口)
@apiGroup DEV
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_elevator_hisdata/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} conditions 过滤条件,必须为JSON格式字符串,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填],支持时间段查询,例如{"CREATED_TIME__gte": "2020-01-07 15:00:00", "CREATED_TIME__lte": "2020-01-07 15:20:00"}, 字段后加上__gte标示大于等于,__lte标示小于等于
@apiSampleRequest http://39.106.148.205/ismsapi/get_elevator_hisdata/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FElevatorID 设备唯一编码,对应获取设备接口的FID
@apiSuccess (结构体) {string} hoist_box_id 黑匣子编号,对应获取设备接口的FDevID
@apiSuccess (结构体) {string} cage_id 吊笼编号
@apiSuccess (结构体) {string} door_lock_state 门锁状态(从右往左数，第0位前门第1位后门，数值1代表开启，0带便关闭。第2位门锁异常指示，0无异常1有异常)
@apiSuccess (结构体) {string} driver_identification_state 身份认证状态
@apiSuccess (结构体) {string} height_percentage 高度百分比
@apiSuccess (结构体) {string} hoist_system_state 系统状态(从右往左数，第0-1位重量，第2-3位高度限位，第4-5位超速，第6-7 位人数，第8-9位倾斜 数值0代表正常，数值1代表预警，数值2代表报警。第10位前门锁状态 第11位后门锁状态:数字0正常,数值1异常)
@apiSuccess (结构体) {string} hoist_time 时间戳
@apiSuccess (结构体) {string} real_time_gradient1 实时倾斜度1
@apiSuccess (结构体) {string} real_time_gradient2 实时倾斜度2
@apiSuccess (结构体) {string} real_time_height 实时高度
@apiSuccess (结构体) {string} real_time_lifting_weight 实时起重量
@apiSuccess (结构体) {string} real_time_number_of_people 实时人数
@apiSuccess (结构体) {string} real_time_or_alarm 结果返回类型,0代表实时值,1代表报警值
@apiSuccess (结构体) {string} real_time_speed 实时速度
@apiSuccess (结构体) {string} real_time_speed_direction 运行方向,方向 0停止1下2上
@apiSuccess (结构体) {string} tilt_percentage1 倾斜百分比1
@apiSuccess (结构体) {string} tilt_percentage2 倾斜百分比2
@apiSuccess (结构体) {string} weight_percentage 重量百分比
@apiSuccess (结构体) {string} system_state 系统状态
@apiSuccess (结构体) {string} wind_speed 实时速度(加工后)
@apiSuccess (结构体) {string} elevator_manager 安全员
@apiSuccess (结构体) {string} elevator_mgrtel 安全员电话
@apiSuccess (结构体) {string} elevator_oper 操作员
@apiSuccess (结构体) {string} wind_speed 操作员电话
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口过滤指定项目的班组
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 通行时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_elevator_hisdata(api_base):
    def set_view(self, request):
        self.model = elevatorinterfacesrv


#获取环境监测实时数据(山东建大仁科)
class get_env_realdata(View):
    def post(self, request):
        APPKEY = request.POST.get('appkey')
        TOKEN = request.POST.get('token')
        PRJ_ID = ''.join(str(request.POST.get('prjid')).split('-'))

        if (APPKEY == None and TOKEN == None):
            reqbody = request.body
            request_json = eval(reqbody.decode())
            APPKEY = request_json['appkey']
            TOKEN = request_json['token']
            PRJ_ID = request_json['prjid']

        response_data = {}

        try:
            appkey_info = T_AppKey.objects.get(Q(FAppkey=APPKEY), Q(FStatus=True))
            response_data = certify_token(APPKEY, TOKEN)

            if response_data['result'] != '0':
                return HttpResponse(json.dumps(response_data))
            else:
                dev_info = device.objects.filter(Q(FStatus=True), Q(CREATED_PRJ=PRJ_ID), Q(FDevtypeID='dc511ffcaaf211e99741708bcdb9b39a'))

                i = 0
                for obj_dev in dev_info:
                    dev_fid = ''.join(str(obj_dev.FID).split('-'))

                    interface_info = devcallinterface.objects.get(Q(FPID=dev_fid), Q(FCallSigCode='GETREALDATA'))
                    initID = ''.join(str(interface_info.FInterfaceID).split('-'))

                    result_run = get_interface_result(initID)
                    response_data['result'] = '0'
                    response_data['msg'] = 'data returned successfully'
                    response_data['data'+str(i)] = result_run
                    i += 1

            return JsonResponse(response_data, safe=False)

        except ObjectDoesNotExist:
            response_data['result'] = '4'
            response_data['msg'] = 'APIKEY serial is UNREGISTERED'

            return HttpResponse(json.dumps(response_data))


#创建项目检查
class create_prjcheck(View):
    def post(self, request):
        content = request.POST.get('content')
        #picfile = request.FILES.get('picfile')

        response_data = {}

        try:
            content = json.loads(content)

            prj_check = prjcheck()
            prj_check.FAddress = content['FAddress']
            prj_check.FPrjID = content['FPrjID']
            prj_check.FProblem = content['FProblem']
            prj_check.FDesc = content['FDesc']
            prj_check.CREATED_TIME = timezone.now()
            prj_check.CREATED_BY = content['CREATED_BY']
            prj_check.UPDATED_BY = content['UPDATED_BY']

            # if picfile != None:
            #     prj_check.FPic = picfile

            prj_check.save()

            response_data['result'] = 0
            response_data['msg'] = '数据添加成功'

            return JsonResponse(response_data, safe=False)
        except Exception as e:
            response_data['result'] = 1
            response_data['msg'] = '数据添加失败'

            return HttpResponse(json.dumps(response_data))


#获取项目检查
class get_prjcheck(View):
    def post(self, request):
        conditions = request.POST.get('conditions')
        response_data = {}

        if conditions != '':
            conditions = json.loads(request.POST.get('conditions'))
            obj = prjcheck.objects.filter(**conditions).order_by("-CREATED_TIME")
        else:
            obj =prjcheck.objects.all().order_by("-CREATED_TIME")

        dict_arr = []

        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            dict.pop("model", None)
            dict.pop("_state", None)
            dict.pop("pk", None)
            dict['FPicFullpath'] = 'http://'+request.get_host()+'/media/'+str(o.FPic)

            dict_arr.append(dict)

        response_data['result'] = '0'
        response_data['msg'] = '数据获取成功'
        response_data['data'] = dict_arr

        return JsonResponse(response_data, safe=False)

#创建检查图片【根据检查项目创建】
class create_prjcheck_pic(View):
    def post(self, request):
        fid = request.POST.get('fid')
        fid = ''.join(str(fid).split('-'))

        picfile = request.FILES.get('picfile')

        response_data = {}

        if fid != '':
            checkpic_info = prjcheckpic()

            checkpic_info.FPID = fid

            if picfile != None:
                checkpic_info.FPic = picfile

            checkpic_info.CREATED_TIME = timezone.now()

            checkpic_info.save()

            response_data['result'] = 0
            response_data['msg'] = '数据添加成功'
        else:
            response_data['result'] = 1
            response_data['msg'] = '数据添加失败，fid不能为空'

        return JsonResponse(response_data, safe=False)

#获取检查图片
class get_prjcheck_pic(api_base):
    def post(self, request):
        conditions = request.POST.get('conditions')
        response_data = {}

        if conditions != '':
            conditions = json.loads(request.POST.get('conditions'))
            obj = prjcheckpic.objects.filter(**conditions).order_by("-CREATED_TIME")
        else:
            obj = prjcheckpic.objects.all().order_by("-CREATED_TIME")

        dict_arr = []

        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            dict.pop("model", None)
            dict.pop("_state", None)
            dict.pop("pk", None)
            dict['FPicFullpath'] = 'http://'+request.get_host()+'/media/'+str(o.FPic)

            dict_arr.append(dict)

        response_data['result'] = '0'
        response_data['msg'] = '数据获取成功'
        response_data['data'] = dict_arr

        return JsonResponse(response_data, safe=False)

#删除检查项目
class delete_prjcheck(View):
    def post(self, request):
        response_data = {}
        try:
            conditions = request.POST.get('conditions')

            if conditions == '':
                obj = prjcheck.objects.all().delete()
            else:
                conditions = json.loads(request.POST.get('conditions'))
                obj = prjcheck.objects.filter(**conditions).delete()

            response_data['result'] = '0'
            response_data['msg'] = '删除成功'

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            response_data['result'] = '1'
            response_data['msg'] = '数据删除失败'

            return JsonResponse(response_data, safe=False)


#删除检查图片
class delete_prjcheck_pic(View):
    def post(self, request):
        response_data = {}
        try:
            conditions = request.POST.get('conditions')

            if conditions == '':
                obj = prjcheckpic.objects.all().delete()
            else:
                conditions = json.loads(request.POST.get('conditions'))
                obj = prjcheckpic.objects.filter(**conditions).delete()

            response_data['result'] = '0'
            response_data['msg'] = '删除成功'

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            response_data['result'] = '1'
            response_data['msg'] = '数据删除失败'

            return JsonResponse(response_data, safe=False)


#获取环境监测历史数据(通用接口)
"""
@api {POST} /ismsapi/get_env_hisdata/ 获取环境监测历史数据(通用接口)
@apiGroup DEV
@apiDescription 调用地址:http://39.106.148.205/ismsapi/get_env_hisdata/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} conditions 过滤条件,必须为JSON格式字符串,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填],支持时间段查询,例如{"FTimestamp__gte": "2020-01-07 15:00:00", "FTimestamp__lte": "2020-01-07 15:20:00"}, 字段后加上__gte标示大于等于,__lte标示小于等于
@apiSampleRequest http://39.106.148.205/ismsapi/get_env_hisdata/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FCommandType 命令类型,2为实时数据
@apiSuccess (结构体) {string} FDeviceId 设备唯一编码,对应获取设备接口的FDevID
@apiSuccess (结构体) {string} FSRCTimestamp 原始时间戳,从设备获取数据的linux格式时间戳,到秒
@apiSuccess (结构体) {string} FTimestamp 时间戳,从设备获取数据的DateTime格式时间戳
@apiSuccess (结构体) {string} FSPM 粉尘数据
@apiSuccess (结构体) {string} FPM25 PM2.5
@apiSuccess (结构体) {string} FPM10 PM10
@apiSuccess (结构体) {string} FWIND_SPEED 风速
@apiSuccess (结构体) {string} FWIND_DIRECT 风向,度数
@apiSuccess (结构体) {string} FWIND_DIRECT_STR 风向,文字
@apiSuccess (结构体) {string} FTemperature 温度
@apiSuccess (结构体) {string} FHumidity 湿度
@apiSuccess (结构体) {string} FNoise 噪音
@apiSuccess (结构体) {string} FNoiseMax 噪音峰值
@apiSuccess (结构体) {string} FLongitude 经度
@apiSuccess (结构体) {string} FLatitude 纬度
@apiSuccess (结构体) {string} FPressure 大气压值
@apiSuccess (结构体) {string} FWIND_SPEED 风速
@apiSuccess (结构体) {string} FWIND_SPEED 风速
@apiSuccess (结构体) {string} FWIND_SPEED 风速
@apiSuccess (结构体) {string} FWIND_SPEED 风速
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目,需要调用项目接口过滤指定项目的班组
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_BY 创建人员
@apiSuccess (结构体) {datetime} CREATED_TIME 通行时间
@apiSuccess (结构体) {datetime} UPDATED_TIME 更新时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class get_env_hisdata(api_base):
    def set_view(self, request):
        self.model = envinterfacesrv


#获取物料台账接口
class get_recepound(api_base):
    def set_view(self, request):
        self.model = materialsaccount

#获取物料台账明细接口
class get_recepound_goodsDetail(api_base):
    def set_view(self, request):
        self.model = materaccountgoods

#获取车辆通行记录接口
class get_vehiclepasslog(api_base):
    def set_view(self, request):
        self.model = vehiclepasslog

#获取车辆通道接口
class get_vehiclegate(api_base):
    def set_view(self, request):
        self.model = vehiclegate

#修改登录密码接口
class modify_user_loginpwd(api_common):
    def set_view(self, request):
        userID = self.request.POST.get('UserID')
        old_pwd = self.request.POST.get('OldPwd')
        new_pwd = self.request.POST.get('NewPwd')
        cfm_pwd = self.request.POST.get('CfmPwd')

        try:
            user_info = User.objects.get(Q(FUserID=userID))

            if old_pwd == user_info.FUserpwd:
                if new_pwd != cfm_pwd:
                    self.response_data['result'] = '8'
                    self.response_data['msg'] = '两次新密码输入不一致'
                else:
                    user_info.FUserpwd = new_pwd
                    user_info.save()

                    self.response_data['result'] = '0'
                    self.response_data['msg'] = '密码修改成功'
            else:
                self.response_data['result'] = '7'
                self.response_data['msg'] = '原始密码错误'

        except ObjectDoesNotExist:
            self.response_data['result'] = '6'
            self.response_data['msg'] = '未找到用户账号'




#创建文件夹、子文件夹
"""
@api {POST} /ismsapi/create_filefolder/ 创建文件夹、子文件夹
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/create_filefolder/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FPRJID 文件夹所属的项目[必填]
@apiParam {string} FPID 创建子文件夹时对应父文件夹的FID[非必填]
@apiParam {string} FFolderNo 文件夹编号[非必填]
@apiParam {string} FFolderName 文件夹名称[必填]
@apiParam {string} FDesc 文件夹描述[非必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/create_filefolder/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FPID 文件夹为子文件时此字段值为父文件夹UUID,如果为空则表示此文件夹为根文件夹
@apiSuccess (结构体) {string} FFolderNo 文件夹编号
@apiSuccess (结构体) {string} FFolderName 文件加名称
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}

"""
class create_filefolder(api_common):
    def set_view(self, request):
        fpid = self.request.POST.get('FPID')
        folderno = self.request.POST.get('FFolderNo')
        foldername = self.request.POST.get('FFolderName')
        desc = self.request.POST.get('FDesc')
        prj_id = self.request.POST.get('FPRJID')

        filefolder_info = filefolder()

        if fpid != None:
            filefolder_info.FPID = fpid

        filefolder_info.FFolderNo = folderno
        filefolder_info.FFolderName = foldername
        filefolder_info.FDesc = desc
        filefolder_info.CREATED_PRJ = prj_id

        org_id = prj_2_manageorg(prj_id)

        filefolder_info.CREATED_ORG = org_id
        filefolder_info.CREATED_BY = 'API'
        filefolder_info.CREATED_TIME = timezone.now()
        filefolder_info.UPDATED_BY = 'API'

        filefolder_info.save()

        data = []
        dict = {}
        dict['FID'] = filefolder_info.FID
        dict['FID_Split'] = ''.join(str(filefolder_info.FID).split('-'))
        dict['FPID'] = filefolder_info.FPID
        dict['FFolderNo'] = filefolder_info.FFolderNo
        dict['FFolderName'] = filefolder_info.FFolderName
        dict['CREATED_PRJ'] = prj_id
        dict['CREATED_ORG'] = org_id

        data.append(dict)

        self.response_data['result'] = '0'
        self.response_data['msg'] = '文件夹创建成功'
        self.response_data['data'] = data


#修改文件夹、子文件夹
"""
@api {POST} /ismsapi/modify_filefolder/ 修改文件夹、子文件夹
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/modify_filefolder/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FID 需要修改的文件夹UUID[必填]
@apiParam {string} FPRJID 文件夹所属的项目[必填]
@apiParam {string} FPID 创建子文件夹时对应父文件夹的FID[非必填]
@apiParam {string} FFolderNo 文件夹编号[非必填]
@apiParam {string} FFolderName 文件夹名称[必填]
@apiParam {string} FDesc 文件夹描述[非必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/modify_filefolder/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FPID 文件夹为子文件时此字段值为父文件夹UUID,如果为空则表示此文件夹为根文件夹
@apiSuccess (结构体) {string} FFolderNo 文件夹编号
@apiSuccess (结构体) {string} FFolderName 文件加名称
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class modify_filefolder(api_common):
    def set_view(self, request):
        fid = self.request.POST.get('FID')

        try:
            filefolder_info = filefolder.objects.get(Q(FID=fid))

            fpid = self.request.POST.get('FPID')
            folderno = self.request.POST.get('FFolderNo')
            foldername = self.request.POST.get('FFolderName')
            desc = self.request.POST.get('FDesc')
            prj_id = self.request.POST.get('FPRJID')

            if fpid != None:
                filefolder_info.FPID = fpid

            if folderno != None:
                filefolder_info.FFolderNo = folderno

            if foldername != None:
                filefolder_info.FFolderName = foldername

            if desc != None:
                filefolder_info.FDesc = desc

            if prj_id != None:
                filefolder_info.CREATED_PRJ = prj_id
                org_id = prj_2_manageorg(prj_id)
                filefolder_info.CREATED_ORG = org_id

            filefolder_info.UPDATED_BY = 'API'

            filefolder_info.save()

            data = []
            dict = {}
            dict['FID'] = filefolder_info.FID
            dict['FID_Split'] = ''.join(str(filefolder_info.FID).split('-'))
            dict['FPID'] = filefolder_info.FPID
            dict['FFolderNo'] = filefolder_info.FFolderNo
            dict['FFolderName'] = filefolder_info.FFolderName
            dict['CREATED_PRJ'] = filefolder_info.CREATED_PRJ
            dict['CREATED_ORG'] = filefolder_info.CREATED_ORG

            data.append(dict)

            self.response_data['result'] = '0'
            self.response_data['msg'] = '文件夹更新成功'
            self.response_data['data'] = data

        except ObjectDoesNotExist:
            self.response_data['result'] = '6'
            self.response_data['msg'] = '文件夹不存在'
            self.response_data['data'] = []

#删除文件夹
"""
@api {POST} /ismsapi/delete_filefolder/ 删除文件夹
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/delete_filefolder/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FID 需要删除的文件夹UUID[必填]
@apiParam {string} TYPE 0:删除当前文件夹1:删除当前文件夹的子文件夹2:删除当前文件夹及其子文件夹
@apiSampleRequest http://121.196.23.69:8090/ismsapi/delete_filefolder/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class delete_filefolder(api_common):
    def set_view(self, request):
        fid = self.request.POST.get('FID')
        type = self.request.POST.get('TYPE')  #0:删除当前文件夹1:删除当前文件夹的子文件夹2:删除当前文件夹及其子文件夹

        if fid != None:
            filefolder_info = filefolder.objects.get(Q(FID=fid))

            if type == '0':
                filefolder_info.delete()
            elif type == '1':
                filefolder_sub_info =  filefolder.objects.filter(Q(FPID=fid))

                for ff_sub in filefolder_sub_info:
                    ff_sub.delete()
            elif type == '2':
                filefolder_sub_info =  filefolder.objects.filter(Q(FPID=fid))

                for ff_sub in filefolder_sub_info:
                    ff_sub.delete()

                filefolder_info.delete()


            self.response_data['result'] = '0'
            self.response_data['msg'] = '文件夹删除成功'
            self.response_data['data'] = []

        else:
            self.response_data['result'] = '6'
            self.response_data['msg'] = '文件夹不存在'
            self.response_data['data'] = []


#查询文件夹、子文件夹
"""
@api {POST} /ismsapi/get_filefolder/ 查询文件夹、子文件夹
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/get_filefolder/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} conditions 过滤条件,必须为JSON格式字符串,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填],支持时间段查询,例如{"FTimestamp__gte": "2020-01-07 15:00:00", "FTimestamp__lte": "2020-01-07 15:20:00"}, 字段后加上__gte标示大于等于,__lte标示小于等于
@apiSampleRequest http://121.196.23.69:8090/ismsapi/get_filefolder/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FPID 文件夹为子文件时此字段值为父文件夹UUID,如果为空则表示此文件夹为根文件夹
@apiSuccess (结构体) {string} FFolderNo 文件夹编号
@apiSuccess (结构体) {string} FFolderName 文件加名称
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class get_filefolder(api_base):
    def set_view(self, request):
        self.model = filefolder


#上传文件至指定的文件夹
"""
@api {POST} /ismsapi/upload_file/ 上传文件至指定的文件夹
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/upload_file/ API接口必须用POST:方法提交,请求类型为：form-data
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FFolderID 目的地文件夹UUID[必填]
@apiParam {string} FPRJID 文件夹所属的项目[必填]
@apiParam {file} FFile 上传的文件内容[必填]
@apiParam {string} FFileType 文件类型[非必填]
@apiParam {string} FFileDesc 文件描述[非必填]
@apiParam {string} FUploader 文件上传人[非必填]
@apiParam {string} FUnionModel 关联模型[非必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/upload_file/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 记录UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FilePath 文件存放物理路径,前面需要拼接http://121.196.23.69:8090/media/
@apiSuccess (结构体) {string} FFolderID 存放的文件夹UUID
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class upload_file(api_common):
    def set_view(self, request):
        prj_id = self.request.POST.get('FPRJID')
        folder_id = self.request.POST.get('FFolderID')
        sfile = self.request.FILES.get('FFile')
        filetype = self.request.POST.get('FFileType')
        filedesc = self.request.POST.get('FFileDesc')
        fileuploader = self.request.POST.get('FUploader')
        unionmodel = self.request.POST.get('FUnionModel')

        if prj_id != None:
            prj_info = project.objects.filter(Q(FID=prj_id))

            if prj_info.count() == 0:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '项目不存在'

                return False
        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '项目ID不能为空'

            return False


        if folder_id != None:
            ffolder_info = filefolder.objects.filter(Q(FID=folder_id))

            if ffolder_info.count() == 0:
                self.response_data['result'] = '21'
                self.response_data['msg'] = '文件夹不存在'

                return False
        else:
            self.response_data['result'] = '20'
            self.response_data['msg'] = '文件夹ID不能为空'

            return False



        if sfile != None:
            ufiles = uploadfiles()
            ufiles.FFolderID = folder_id
            ufiles.FFile = sfile
            ufiles.FFileType = filetype
            ufiles.FFileDesc = filedesc
            ufiles.FUploader = fileuploader
            ufiles.FUnionBimModel = unionmodel

            ufiles.CREATED_PRJ = prj_id

            org_id = prj_2_manageorg(prj_id)
            ufiles.CREATED_ORG = org_id
            ufiles.CREATED_BY = 'API'
            ufiles.CREATED_TIME = timezone.now()
            ufiles.UPDATED_BY = 'API'
            ufiles.save()

            data = []
            dict = {}
            dict['FID'] = ufiles.FID
            dict['FID_Split'] = ''.join(str(ufiles.FID).split('-'))
            dict['FilePath'] = str(ufiles.FFile)
            dict['FFolderID'] = ufiles.FFolderID
            dict['FFileDesc'] = ufiles.FFileDesc
            dict['FUploader'] = ufiles.FUploader
            dict['FUnionModel'] = ufiles.FUnionBimModel
            dict['CREATED_PRJ'] = prj_id
            dict['CREATED_ORG'] = org_id
            dict['CREATED_TIME'] = ufiles.CREATED_TIME

            data.append(dict)

            self.response_data['result'] = 0
            self.response_data['msg'] = '数据添加成功'
            self.response_data['data'] = data
        else:
            self.response_data['result'] = '30'
            self.response_data['msg'] = '上传文件不能为空'

            return False

        return True


#获取文件夹内文件列表
"""
@api {POST} /ismsapi/get_folder_infiles/ 获取文件夹内文件列表
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/get_folder_infiles/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FFolderID 文件夹UUID[必填]
@apiParam {string} FPRJID 项目UUID[必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/get_folder_infiles/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FILES_ID 文件UUID，唯一标识
@apiSuccess (结构体) {string} FILES_ID_Splite 去分割符后的UUID
@apiSuccess (结构体) {string} FILES_PATH 文件存放物理路径,前面需要拼接http://121.196.23.69:8090/media/
@apiSuccess (结构体) {string} FILES_FOLDERID 存放的文件夹UUID
@apiSuccess (结构体) {string} FILES_TYPEID 文件类型
@apiSuccess (结构体) {string} FILES_DESC 文件描述
@apiSuccess (结构体) {string} FILES_UPLOADER 文件上传人
@apiSuccess (结构体) {string} FILES_UNIONMODEL 关联模型
@apiSuccess (结构体) {string} CREATED_TIME 上传时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class get_folder_infiles(api_common):
    def set_view(self, request):
        prj_id = self.request.POST.get('FPRJID')
        folder_id = self.request.POST.get('FFolderID')

        if prj_id != None:
            prj_info = project.objects.filter(Q(FID=prj_id))

            if prj_info.count() == 0:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '项目不存在'

                return False
        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '项目ID不能为空'

            return False


        if folder_id != None:
            ffolder_info = filefolder.objects.filter(Q(FID=folder_id))

            if ffolder_info.count() == 0:
                self.response_data['result'] = '21'
                self.response_data['msg'] = '文件夹不存在'

                return False
        else:
            self.response_data['result'] = '20'
            self.response_data['msg'] = '文件夹ID不能为空'

            return False

        ufiles_info = uploadfiles.objects.filter(Q(FFolderID=folder_id))

        data = []
        for ufiles in ufiles_info:
            dict = {}

            dict['FILES_ID'] = ufiles.FID
            dict['FILES_ID_Splite'] = ''.join(str(ufiles.FID).split('-'))
            dict['FILES_FOLDERID'] = ufiles.FFolderID
            dict['FILES_PATH'] = str(ufiles.FFile)
            dict['FILES_DESC'] = ufiles.FFileDesc
            dict['FILES_TYPEID'] = ufiles.FFileType
            dict['FILES_UPLOADER'] = ufiles.FUploader
            dict['FILES_UNIONMODEL'] = ufiles.FUnionBimModel
            dict['CREATED_TIME'] = ufiles.CREATED_TIME

            data.append(dict)

        self.response_data['result'] = 0
        self.response_data['msg'] = '数据查询成功'
        self.response_data['data'] = data


#删除指定文件
"""
@api {POST} /ismsapi/delete_files/ 删除指定文件
@apiGroup FILE
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/delete_files/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FFilesID 文件UUID[选填]
@apiParam {string} FFolderID 文件夹UUID[选填]
@apiParam {string} FPRJID 项目UUID[选填]
@apiParam {string} MODE [必填]0:删除指定文件 1:删除指定文件夹内所有文件 2：删除指定项目内的所有文件
@apiSampleRequest http://121.196.23.69:8090/ismsapi/delete_files/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class delete_files(api_common):
    def set_view(self, request):
        file_id = self.request.POST.get('FFilesID')
        folder_id = self.request.POST.get('FFolderID')
        prj_id = self.request.POST.get('FPRJID')
        mode = self.request.POST.get('MODE')   #0:删除指定文件 1:删除指定文件夹内所有文件 2：删除指定项目内的所有文件

        if mode == None:
            self.response_data['result'] = '30'
            self.response_data['msg'] = 'MODE参数必须传值'
            self.response_data['data'] = []

            return False

        if mode == '0':
            if file_id != None:
                file_info = uploadfiles.objects.filter(Q(FID=file_id))

                if file_info.count() == 0:
                    self.response_data['result'] = '11'
                    self.response_data['msg'] = '文件不存在'

                    return False
                else:
                    __file_info =  file_info.first()

                    file_path = settings.MEDIA_ROOT+"/"+str(__file_info.FFile)
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    file_info.delete()

                    self.response_data['result'] = 0
                    self.response_data['msg'] = '数据删除成功'
                    self.response_data['data'] = []

                    return True
            else:
                self.response_data['result'] = '10'
                self.response_data['msg'] = '文件ID不能为空'

                return False

        elif mode == '1':
            if folder_id != None:
                ffolder_info = filefolder.objects.filter(Q(FID=folder_id))

                if ffolder_info.count() == 0:
                    self.response_data['result'] = '21'
                    self.response_data['msg'] = '文件夹不存在'

                    return False
                else:
                    files_info = uploadfiles.objects.filter(Q(FFolderID=folder_id))

                    for files in files_info:
                        file_path = settings.MEDIA_ROOT + "/" + str(files.FFile)
                        if os.path.exists(file_path):
                            os.remove(file_path)

                        files.delete()

                    self.response_data['result'] = 0
                    self.response_data['msg'] = '数据删除成功'
                    self.response_data['data'] = []

                    return True
            else:
                self.response_data['result'] = '20'
                self.response_data['msg'] = '文件夹ID不能为空'

                return False

        elif mode == '2':
            if prj_id != None:
                prj_info = project.objects.filter(Q(FID=prj_id))

                if prj_info.count() == 0:
                    self.response_data['result'] = '11'
                    self.response_data['msg'] = '项目不存在'

                    return False
                else:
                    files_info = uploadfiles.objects.filter(Q(CREATED_PRJ=prj_id))
                    files_info.delete()

                    self.response_data['result'] = 0
                    self.response_data['msg'] = '数据删除成功'
                    self.response_data['data'] = []

                    return True
            else:
                self.response_data['result'] = '10'
                self.response_data['msg'] = '项目ID不能为空'

                return False


# 获取手动抓图路径【正邦业务】
class get_CapturePicURL(api_common):
    def set_view(self, request):
        try:
            host_ip = self.request.get_host()
            dev_id = self.request.POST.get('DEVID')
            channel_no = self.request.POST.get('CHANNELNO')

            if dev_id == None:
                self.response_data['result'] = '10'
                self.response_data['msg'] = 'DEVID参数必须传值'
                self.response_data['data'] = []

                return False

            if channel_no == None:
                self.response_data['result'] = '10'
                self.response_data['msg'] = 'CHANNELNO参数必须传值'
                self.response_data['data'] = []

                return False

            tasklist_info = tasklist()

            tasklist_info.FDevID = dev_id
            tasklist_info.FChannelNo = channel_no

            if self.request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = self.request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                ip = self.request.META.get('REMOTE_ADDR')

            tasklist_info.CREATED_BY = ip
            tasklist_info.UPDATED_BY = ip
            tasklist_info.CREATED_TIME = timezone.now()

            tasklist_info.save()

            pic_id = ''.join(str(tasklist_info.FID).split('-'))

            self.response_data['result'] = '0'
            self.response_data['msg'] = 'success'

            dict = {}
            dict['URL'] = '/media/itemcheckpic/'+pic_id+'.jpg'
            data = []
            data.append(dict)

            self.response_data['data'] = data

            return True

        except Exception as e:
            self.response_data['result'] = '20'
            self.response_data['msg'] = str(e)

            return False


# 工控设备心跳包
class get_heartbeat(api_common):
    def set_view(self, request):
        dev_id = self.request.POST.get('DEVID')

        if dev_id == None:
            self.response_data['result'] = '10'
            self.response_data['msg'] = 'DEVID参数必须传值'
            self.response_data['data'] = []

            return False

        try:
            tasklist_info = tasklist.objects.filter(Q(FDevID=dev_id))

            data = []
            for _list in tasklist_info:
                dict = {}

                dict['DEVID'] = dev_id
                dict['TaskType'] = _list.FTaskType
                dict['Scope'] = _list.FScope
                dict['CHANNELNO'] = _list.FChannelNo
                dict['PICID'] = ''.join(str(_list.FID).split('-'))

                data.append(dict)

            tasklist_info.delete()

            self.response_data['result'] = '0'
            self.response_data['msg'] = 'success'
            self.response_data['data'] = data

            return True

        except Exception as e:
            pass

# 新增/修改协同
"""
@api {POST} /ismsapi/add_teamworker/ 新增/修改协同
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/add_teamworker/ API接口必须用POST:方法提交,请求类型为：form-data
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FPRJID 项目UUID[必填]
@apiParam {string} FTeamWorkerTypeID 协作类型[必填]
@apiParam {string} ACTION 操作类型[必填]0:新增,1:修改
@apiParam {string} FTEAMWORKER_ID 需要修改的协同UUID[必填],当ACTION为1时必填
@apiParam {string} FTitle 协同主题[必填]
@apiParam {string} FDeadLine 限期[选填]
@apiParam {string} FLevel 优先级[选填]
@apiParam {string} FTag 标识[选填]
@apiParam {string} FBimModel 关联BIM[选填]
@apiParam {string} FPic 关联图片或文件[选填],form-data,File类型
@apiParam {string} FRecord 录音文件[选填],form-data,File类型
@apiParam {string} FStakeholder 关联干系人[选填]
@apiParam {string} FDesc 描述[选填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/add_teamworker/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 协同UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerTypeID 协作类型UUID
@apiSuccess (结构体) {string} FTeamWorkerType 协作类型
@apiSuccess (结构体) {string} FTitle 协同主题
@apiSuccess (结构体) {string} FDeadLine 限期
@apiSuccess (结构体) {string} FLevel 优先级
@apiSuccess (结构体) {string} FTag 标识
@apiSuccess (结构体) {string} FBimModel 关联BIM[选填]
@apiSuccess (结构体) {string} FPic 关联图片或文件[选填],form-data,File类型
@apiSuccess (结构体) {string} FRecord 录音文件[选填],form-data,File类型
@apiSuccess (结构体) {string} FStakeholder 关联干系人[选填]
@apiSuccess (结构体) {string} FDesc 描述[选填]
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class add_teamworker(api_common):
    def set_view(self, request):
        prj_id = self.request.POST.get('FPRJID')
        typeID = self.request.POST.get('FTeamWorkerTypeID')
        title = self.request.POST.get('FTitle')
        deadline = self.request.POST.get('FDeadLine')
        level = self.request.POST.get('FLevel')
        tag = self.request.POST.get('FTag')
        bimmodel = self.request.POST.get('FBimModel')
        picfile = self.request.FILES.get('FPic')
        recordfile = self.request.FILES.get('FRecord')
        stakeholder = self.request.POST.get('FStakeholder')
        desc = self.request.POST.get('FDesc')
        action = self.request.POST.get('ACTION')
        teamworkerID = self.request.POST.get('FTEAMWORKER_ID')
        created_by = self.request.POST.get('CREATED_BY')

        if action == None:
            self.response_data['result'] = '12'
            self.response_data['msg'] = 'ACTION不能为空'

            return False

        if prj_id != None:
            prj_info = project.objects.filter(Q(FID=prj_id))

            if prj_info.count() == 0:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '项目不存在'

                return False
        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '项目ID不能为空'

            return False


        if typeID != None:
            type_info = base.objects.filter(Q(FID=typeID))

            if type_info.count() == 0:
                self.response_data['result'] = '21'
                self.response_data['msg'] = '协作类型不存在'

                return False
        else:
            self.response_data['result'] = '20'
            self.response_data['msg'] = '协作类型不能为空'

            return False


        if title == None:
            self.response_data['result'] = '31'
            self.response_data['msg'] = '协作主题不能为空'

            return False


        if action == '0':    # 新增
            teamworker_info =teamworker()
        elif action == '1':  # 修改
            try:
                teamworker_info = teamworker.objects.get(Q(FID=teamworkerID))

            except ObjectDoesNotExist:
                self.response_data['result'] = '22'
                self.response_data['msg'] = '要修改的协同ID不存在'

                return False
        else:
            teamworker_info = teamworker()

        teamworker_info.FTeamWorkerTypeID = typeID
        teamworker_info.FTitle = title
        teamworker_info.FDeadLine = deadline
        teamworker_info.FLevel = level
        teamworker_info.FTag = tag
        teamworker_info.FBimModel = bimmodel
        teamworker_info.FPic = picfile
        teamworker_info.FRecord = recordfile
        teamworker_info.FStakeholder = stakeholder
        teamworker_info.FDesc = desc
        teamworker_info.FStatus = 1
        teamworker_info.CREATED_PRJ = prj_id
        # teamworker_info.FClassifyTag = classifytag

        org_id = prj_2_manageorg(prj_id)

        teamworker_info.CREATED_ORG = org_id

        if created_by == None:
            teamworker_info.CREATED_BY = 'API'
        else:
            teamworker_info.CREATED_BY = created_by

        teamworker_info.UPDATED_BY = 'API'
        teamworker_info.CREATED_TIME = timezone.now()

        teamworker_info.save()

        data = []
        dict = {}
        dict['FID'] = teamworker_info.FID
        dict['FID_Split'] = ''.join(str(teamworker_info.FID).split('-'))
        dict['FTeamWorkerTypeID'] = teamworker_info.FTeamWorkerTypeID
        dict['FTeamWorkerType'] = type_info.first().FBase
        dict['FTitle'] = title
        dict['FDeadLine'] = deadline
        dict['FLevel'] = level
        dict['FTag'] = tag
        dict['FBimModel'] = bimmodel
        dict['FPic'] = str(picfile)
        dict['FRecord'] = str(recordfile)
        dict['FStakeholder'] = stakeholder
        dict['FDesc'] = desc
        dict['CREATED_PRJ'] = prj_id
        dict['CREATED_ORG'] = org_id
        dict['CREATED_BY'] = 'API'
        dict['UPDATED_BY'] = 'API'
        dict['CREATED_TIME'] = timezone.now()

        data.append(dict)

        self.response_data['result'] = 0

        if action == '0':
            self.response_data['msg'] = '数据添加成功'
        elif action == '1':
            self.response_data['msg'] = '数据更新成功'

        self.response_data['data'] = data

        return


# 查询返回指定协同
"""
@api {POST} /ismsapi/get_teamworker/ 查询协同
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/get_teamworker/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} conditions 过滤条件,必须为JSON格式字符串,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填],支持时间段查询,例如{"FTimestamp__gte": "2020-01-07 15:00:00", "FTimestamp__lte": "2020-01-07 15:20:00"}, 字段后加上__gte标示大于等于,__lte标示小于等于
@apiSampleRequest http://121.196.23.69:8090/ismsapi/get_teamworker/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 协同UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerTypeID 协作类型UUID
@apiSuccess (结构体) {string} FTeamWorkerType 协作类型
@apiSuccess (结构体) {string} FTitle 协同主题
@apiSuccess (结构体) {string} FDeadLine 限期
@apiSuccess (结构体) {string} FLevel 优先级
@apiSuccess (结构体) {string} FTag 标识
@apiSuccess (结构体) {string} FBimModel 关联BIM[选填]
@apiSuccess (结构体) {string} FPic 关联图片或文件[选填],form-data,File类型
@apiSuccess (结构体) {string} FRecord 录音文件[选填],form-data,File类型
@apiSuccess (结构体) {string} FStakeholder 关联干系人[选填]
@apiSuccess (结构体) {string} FDesc 描述[选填]
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiSuccess (结构体) {string} UPDATE_TIME 修改时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class get_teamworker(api_base):
    def set_view(self, request):
        self.model = teamworker


# 删除指定协同
"""
@api {POST} /ismsapi/delete_teamworker/ 删除指定协同
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/delete_teamworker/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FTEAMWORKER_ID 协同UUID[选填]
@apiParam {string} FPRJID 项目UUID[选填]
@apiParam {string} MODE [必填]0:删除指定协同2：删除指定项目内的所有协同
@apiSampleRequest http://121.196.23.69:8090/ismsapi/delete_teamworker/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class delete_teamworker(api_common):
    def set_view(self, request):
        teamworker_id = self.request.POST.get('FTEAMWORKER_ID')
        prj_id = self.request.POST.get('FPRJID')
        mode = self.request.POST.get('MODE')   #0:删除指定协同 1：删除指定项目内的所有协同

        if mode == None:
            self.response_data['result'] = '30'
            self.response_data['msg'] = 'MODE参数必须传值'
            self.response_data['data'] = []

            return False


        if mode == '0':
            if teamworker_id != None:
                teamworker_info = teamworker.objects.filter(Q(FID=teamworker_id))

                if teamworker_info.count() == 0:
                    self.response_data['result'] = '11'
                    self.response_data['msg'] = '协同不存在'

                    return False
                else:
                    teamworker_info.delete()

                    self.response_data['result'] = 0
                    self.response_data['msg'] = '数据删除成功'
                    self.response_data['data'] = []

                    return True
            else:
                self.response_data['result'] = '10'
                self.response_data['msg'] = '协同ID不能为空'

                return False

        elif mode == '1':
            if prj_id != None:
                prj_info = project.objects.filter(Q(FID=prj_id))

                if prj_info.count() == 0:
                    self.response_data['result'] = '11'
                    self.response_data['msg'] = '项目不存在'

                    return False
                else:
                    teamwoer_info = teamworker.objects.filter(Q(CREATED_PRJ=prj_id))
                    teamwoer_info.delete()

                    self.response_data['result'] = 0
                    self.response_data['msg'] = '数据删除成功'
                    self.response_data['data'] = []

                    return True
            else:
                self.response_data['result'] = '10'
                self.response_data['msg'] = '项目ID不能为空'

                return False


# 新增/修改协同类型
"""
@api {POST} /ismsapi/add_teamworkerType/ 新增/修改协同类型
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/add_teamworkerType/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FTeamWorkerType 协作类型[必填]
@apiParam {string} ACTION 操作类型[必填]0:新增,1:修改
@apiParam {string} FTeamWorkerTypeID 需要修改的协作类型UUID[必填],当ACTION为1时必填
@apiSampleRequest http://121.196.23.69:8090/ismsapi/add_teamworkerType/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 协作类型UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FBaseID 协作类型编码
@apiSuccess (结构体) {string} FBase 协作类型
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class add_teamworkerType(api_common):
    def set_view(self, request):
        tw_type = self.request.POST.get('FTeamWorkerType')
        action = self.request.POST.get('ACTION')
        typeID = self.request.POST.get('FTeamWorkerTypeID')

        if action == None:
            self.response_data['result'] = '12'
            self.response_data['msg'] = 'ACTION不能为空'

            return False

        if tw_type != None:
            if action == '0':     # 新增协同类型
                base_info = base()
            elif action == '1':   # 修改协同类型
                try:
                    base_info = base.objects.get(Q(FID=typeID))
                except ObjectDoesNotExist:
                    self.response_data['result'] = '13'
                    self.response_data['msg'] = 'FTeamWorkerTypeID不能为空'

                    return False
            else:
                base_info = base()


            base_info.FPID = 'b584392ab52a11eaa21300163e0b36b4'

            if action == '0':
                baseID = gensequence('api_add_teamworkerType', '8000.', 3, 0)
                base_info.FBaseID = baseID
            else:
                baseID = ''

            base_info.FBase = tw_type
            base_info.CREATED_BY = 'API'
            base_info.UPDATED_BY = 'API'
            base_info.CREATED_TIME = timezone.now()

            base_info.save()

            data = []
            dict = {}
            dict['FID'] = base_info.FID
            dict['FID_Split'] = ''.join(str(base_info.FID).split('-'))
            dict['FBaseID'] = baseID
            dict['FBase'] = tw_type
            dict['CREATED_BY'] = 'API'
            dict['UPDATED_BY'] = 'API'
            dict['CREATED_TIME'] = timezone.now()

            data.append(dict)

            self.response_data['result'] = 0

            if action == '0':
                self.response_data['msg'] = '数据添加成功'
            elif action == '1':
                self.response_data['msg'] = '数据更新成功'

            self.response_data['data'] = data

            return

        else:
            self.response_data['result'] = '20'
            self.response_data['msg'] = '协作类型不能为空'

            return False

# 查询协同类型
"""
@api {POST} /ismsapi/get_teamworkerType/ 查询协同类型
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/get_teamworkerType/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/get_teamworkerType/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 协同UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FBaseID 协作类型编码
@apiSuccess (结构体) {string} FBase 协作类型
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiSuccess (结构体) {string} UPDATE_TIME 修改时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class get_teamworkerType(api_common):
    def set_view(self, request):

        base_info = base.objects.filter(Q(FPID='b584392ab52a11eaa21300163e0b36b4'))

        self.response_data['result'] = '0'
        self.response_data['msg'] = 'success'
        self.response_data['data'] = convert_to_dicts(base_info)


# 删除协同类型
"""
@api {POST} /ismsapi/delete_teamworkerType/ 删除指定协同类型
@apiGroup TEAMWORKER 
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/delete_teamworkerType/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FTeamWorkerTypeID 协同类型UUID[必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/delete_teamworkerType/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class delete_teamworkerType(api_common):
    def set_view(self, request):

        typeID = self.request.POST.get('FTeamWorkerTypeID')

        try:
            base_info = base.objects.get(Q(FID=typeID))
            base_info.delete()

            self.response_data['result'] = '0'
            self.response_data['msg'] = '删除数据成功'
            self.response_data['data'] = []

        except ObjectDoesNotExist:
            self.response_data['result'] = '10'
            self.response_data['msg'] = 'FTeamWorkerTypeID不存在'

            return



# 新增/编辑协同回复内容
"""
@api {POST} /ismsapi/add_teamworker_reply/ 新增/编辑协同回复内容
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/add_teamworker_reply/ API接口必须用POST:方法提交,请求类型为：form-data
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FTEAMWORKERID 协同UUID[必填]
@apiParam {string} ACTION 操作类型[必填]0:新增回复,1:编辑回复
@apiParam {string} FReplyPerson 回复人[必填]
@apiParam {string} FReply 回复内容[必填]
@apiParam {string} FStakeholder 干系人[选填]就是本条回复需要at的人,每个干系人之间用逗号隔开
@apiParam {string} FPic 关联图片或文件[选填],form-data,File类型
@apiParam {string} FRecord 录音文件[选填],form-data,File类型
@apiSampleRequest http://121.196.23.69:8090/ismsapi/add_teamworker_reply/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 本条回复内容UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerID 协同UUID
@apiSuccess (结构体) {string} FReply 回复内容
@apiSuccess (结构体) {string} FPic 回复图片
@apiSuccess (结构体) {string} FRecord 回复录音
@apiSuccess (结构体) {string} FStakeholder at干系人
@apiSuccess (结构体) {string} FReadTag 阅读标记0未读，1已读
@apiSuccess (结构体) {string} FReplyPerson 回复人
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 所属组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class add_teamworker_reply(api_common):
    def set_view(self, request):

        teamworkerID = self.request.POST.get('FTEAMWORKERID')
        twreplyID = self.request.POST.get('FTWREPLYID')
        replyMan = self.request.POST.get('FReplyPerson')
        replyMemo = self.request.POST.get('FReply')
        stakeholder = self.request.POST.get('FStakeholder')
        picfile = self.request.FILES.get('FPic')
        recordfile = self.request.FILES.get('FRecord')
        action = self.request.POST.get('ACTION')

        if action == None:
            self.response_data['result'] = '12'
            self.response_data['msg'] = 'ACTION不能为空'

            return False

        if teamworkerID != None:
            try:
                teamworker_info = teamworker.objects.get(Q(FID=teamworkerID))
            except ObjectDoesNotExist:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '协同不存在'

                return

        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '协同ID不能为空'

            return False


        if replyMan == None:
            self.response_data['result'] = '13'
            self.response_data['msg'] = '回复人不能为空'

            return False

        if replyMemo == None:
            self.response_data['result'] = '14'
            self.response_data['msg'] = '回复内容不能为空'

            return False


        if action == '0':    # 新增
            reply_info = teamworkreply()
        elif action == '1':  # 修改
            try:
                reply_info = teamworkreply.objects.get(Q(FID=twreplyID))

            except ObjectDoesNotExist:
                self.response_data['result'] = '22'
                self.response_data['msg'] = '要编辑的回复ID不存在'

                return False
        else:
            reply_info = teamworkreply()


        if action == '0':
            reply_info.FTeamWorkerID = teamworkerID
            reply_info.FReply = replyMemo
            reply_info.FPic = picfile
            reply_info.FRecord = recordfile
            reply_info.FStakeholder = stakeholder
            reply_info.FReadTag = 0
            reply_info.FReplyPerson = replyMan

            reply_info.CREATED_PRJ = teamworker_info.CREATED_PRJ
            reply_info.CREATED_ORG = teamworker_info.CREATED_ORG
            reply_info.CREATED_BY = 'API'
            reply_info.UPDATED_BY = 'API'
            reply_info.CREATED_TIME = timezone.now()

        else:
            reply_info.FReply = replyMemo
            reply_info.FPic = picfile
            reply_info.FRecord = recordfile
            reply_info.FReadTag = 0

            reply_info.CREATED_TIME = timezone.now()

        reply_info.save()

        teamworker_info.FClassifyTag = 1
        teamworker_info.save()

        data = []
        dict = {}
        dict['FID'] = reply_info.FID
        dict['FID_Split'] = ''.join(str(reply_info.FID).split('-'))
        dict['FTeamWorkerID'] = reply_info.FTeamWorkerID
        dict['FReply'] = reply_info.FReply
        dict['FPic'] = str(picfile)
        dict['FRecord'] = str(recordfile)
        dict['FStakeholder'] = reply_info.FStakeholder
        dict['FReadTag'] = reply_info.FReadTag
        dict['FReplyPerson'] = reply_info.FReplyPerson
        dict['CREATED_PRJ'] = reply_info.CREATED_PRJ
        dict['CREATED_ORG'] = reply_info.CREATED_ORG
        dict['CREATED_BY'] = 'API'
        dict['UPDATED_BY'] = 'API'
        dict['CREATED_TIME'] = reply_info.CREATED_TIME

        data.append(dict)

        self.response_data['result'] = 0

        if action == '0':
            self.response_data['msg'] = '数据添加成功'
        elif action == '1':
            self.response_data['msg'] = '数据更新成功'

        self.response_data['data'] = data

        return



# 查询协同回复内容
"""
@api {POST} /ismsapi/get_teamworker_reply/ 查询协同回复内容
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/get_teamworker_reply/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FTEAMWORKERID 协同UUID[必填]
@apiSampleRequest http://121.196.23.69:8090/ismsapi/get_teamworker_reply/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 回复内容UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerID 协同UUID
@apiSuccess (结构体) {string} FReply 回复内容
@apiSuccess (结构体) {string} FPic 回复图片
@apiSuccess (结构体) {string} FRecord 回复录音
@apiSuccess (结构体) {string} FStakeholder at干系人
@apiSuccess (结构体) {string} FReadTag 阅读标记0未读，1已读
@apiSuccess (结构体) {string} FReplyPerson 回复人
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 所属组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class get_teamworker_reply(api_common):
    def set_view(self, request):

        teamworkerID = self.request.POST.get('FTEAMWORKERID')

        if teamworkerID != None:
            try:
                teamworker_info = teamworker.objects.get(Q(FID=teamworkerID))
            except ObjectDoesNotExist:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '协同不存在'

                return

        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '协同ID不能为空'

            return False


        reply_info = teamworkreply.objects.filter(Q(FTeamWorkerID=teamworkerID))

        self.response_data['result'] = '0'
        self.response_data['msg'] = 'success'
        self.response_data['data'] = convert_to_dicts(reply_info)


# 返回@人员消息
"""
@api {POST} /ismsapi/get_temworker_atReply/ 返回查询at人员消息
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/get_temworker_atReply/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FStakeholder at干系人[必填]
@apiParam {string} conditions 过滤条件,必须为JSON格式字符串,例如{"条件":"值", "条件","值"},不传递此参数则不进行过滤获取全部数据[选填],支持时间段查询,例如{"FTimestamp__gte": "2020-01-07 15:00:00", "FTimestamp__lte": "2020-01-07 15:20:00"}, 字段后加上__gte标示大于等于,__lte标示小于等于
@apiSampleRequest http://121.196.23.69:8090/ismsapi/get_temworker_atReply/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 回复内容UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerID 协同UUID
@apiSuccess (结构体) {string} FReply 回复内容
@apiSuccess (结构体) {string} FPic 回复图片
@apiSuccess (结构体) {string} FRecord 回复录音
@apiSuccess (结构体) {string} FStakeholder at干系人
@apiSuccess (结构体) {string} FReadTag 阅读标记0未读，1已读
@apiSuccess (结构体) {string} FReplyPerson 回复人
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 所属组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class get_temworker_atReply(api_common):
    def set_view(self, request):

        stakeholder = self.request.POST.get('FStakeholder')
        conditions = self.request.POST.get('conditions')

        if stakeholder != None:
            reply_info = teamworkreply.objects.filter(Q(FStakeholder__contains=stakeholder))

            if conditions != None:
                conditions = json.loads(conditions)
                reply_info = reply_info.filter(**conditions)

            self.response_data['result'] = '0'
            self.response_data['msg'] = 'success'
            self.response_data['data'] = convert_to_dicts(reply_info)

            return

        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '@人员不能为空'

            return False


# 标记回复内容已读/未读
"""
@api {POST} /ismsapi/marke_replyreadtag/ 标记回复内容已读未读
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/marke_replyreadtag/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FREPLYID 回复UUID[必填]
@apiParam {string} ACTION 已读/未读标记[必填],0:未读，1:已读
@apiSampleRequest http://121.196.23.69:8090/ismsapi/marke_replyreadtag/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 回复内容UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerID 协同UUID
@apiSuccess (结构体) {string} FReply 回复内容
@apiSuccess (结构体) {string} FPic 回复图片
@apiSuccess (结构体) {string} FRecord 回复录音
@apiSuccess (结构体) {string} FStakeholder at干系人
@apiSuccess (结构体) {string} FReadTag 阅读标记0未读，1已读
@apiSuccess (结构体) {string} FReplyPerson 回复人
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 所属组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class marke_replyreadtag(api_common):
    def set_view(self, request):

        replyID = self.request.POST.get('FREPLYID')
        action = self.request.POST.get('ACTION')

        if replyID != None:
            try:
                reply_info = teamworkreply.objects.get(Q(FID=replyID))
            except ObjectDoesNotExist:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '回复内容不存在'

                return

        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '回复UUID不能为空'

            return False


        if action == None:
            self.response_data['result'] = '12'
            self.response_data['msg'] = 'ACTION不能为空'

            return False


        if action == '0':   # 未读
            reply_info.FReadTag = 0
        elif action == '1': # 已读
            reply_info.FReadTag = 1
        else:
            self.response_data['result'] = '13'
            self.response_data['msg'] = 'ACTION只能传0或1'

            return False

        reply_info.save()

        reply_info = teamworkreply.objects.filter(Q(FID=replyID))

        self.response_data['result'] = '0'
        self.response_data['msg'] = 'success'
        self.response_data['data'] = convert_to_dicts(reply_info)


# 审核/取消审核协同
"""
@api {POST} /ismsapi/approve_teamworker/ 审核,取消审核协同
@apiGroup TEAMWORKER
@apiDescription 调用地址:http://121.196.23.69:8090/ismsapi/approve_teamworker/ API接口必须用POST:方法提交,请求类型为：x-www-form-urlencoded
@apiParam {string} appkey 在后台管理系统中注册的APPKEY[必填]
@apiParam {string} token 对应该appkey的有效token, token的有效期为一小时[必填]
@apiParam {string} FTEAMWORKERID 协同UUID[必填]
@apiParam {string} FApproveMemo 审核内容[选填]
@apiParam {string} ACTION 操作类型[必填]0:审核,1:取消审核
@apiSampleRequest http://121.196.23.69:8090/ismsapi/approve_teamworker/
@apiSuccess (返回消息) {string} result 返回码
@apiSuccess (返回消息) {string} msg 返回消息
@apiSuccess (返回消息) {string} data 安全规则结构体
@apiSuccess (消息内容) {string} 0 数据获取成功
@apiSuccess (消息内容) {string} 1 token过期
@apiSuccess (消息内容) {string} 2 token校验失败
@apiSuccess (消息内容) {string} 3 token校验传递参数错误
@apiSuccess (消息内容) {string} 4 APPKEY未注册,或被禁用
@apiSuccess (消息内容) {string} 5 API接口必须用POST方法提交
@apiSuccess (结构体) {string} FID 协同UUID，唯一标识
@apiSuccess (结构体) {string} FID_Split 去分割符后的UUID
@apiSuccess (结构体) {string} FTeamWorkerTypeID 协作类型UUID
@apiSuccess (结构体) {string} FTeamWorkerType 协作类型
@apiSuccess (结构体) {string} FTitle 协同主题
@apiSuccess (结构体) {string} FDeadLine 限期
@apiSuccess (结构体) {string} FLevel 优先级
@apiSuccess (结构体) {string} FTag 标识
@apiSuccess (结构体) {string} FBimModel 关联BIM[选填]
@apiSuccess (结构体) {string} FPic 关联图片或文件[选填],form-data,File类型
@apiSuccess (结构体) {string} FRecord 录音文件[选填],form-data,File类型
@apiSuccess (结构体) {string} FStakeholder 关联干系人[选填]
@apiSuccess (结构体) {string} FDesc 描述[选填]
@apiSuccess (结构体) {string} FClassifyTag 分类标记0：待整改，1：进行中【创建了回复，该协同自动变成此状态】，2:已完成【审批通过，该协同自动变成此状态】
@apiSuccess (结构体) {string} CREATED_PRJ 所属项目
@apiSuccess (结构体) {string} CREATED_ORG 创建组织
@apiSuccess (结构体) {string} CREATED_TIME 创建时间
@apiSuccess (结构体) {string} UPDATE_TIME 修改时间
@apiErrorExample {json} 错误返回样例：
{"result": "1", "msg": "token has expired"}
{"result": "2", "msg": "token validation failed"}
{"result": "3", "msg": "args illegal"}
{"result": "4", "msg": "APPKEY serial is UNREGISTERED"}
{"result": "5", "msg": "API interface must be submitted by post method."}
"""
class approve_teamworker(api_common):
    def set_view(self, request):

        teamworkerID = self.request.POST.get('FTEAMWORKERID')
        approveMemo = self.request.POST.get('FApproveMemo')
        action = self.request.POST.get('ACTION')

        if teamworkerID != None:
            try:
                teamworker_info = teamworker.objects.get(Q(FID=teamworkerID))
            except ObjectDoesNotExist:
                self.response_data['result'] = '11'
                self.response_data['msg'] = '协同不存在'

                return

        else:
            self.response_data['result'] = '10'
            self.response_data['msg'] = '协同ID不能为空'

            return False


        if action == None:
            self.response_data['result'] = '12'
            self.response_data['msg'] = 'ACTION不能为空'

            return False


        if action == '0':   # 审核
            teamworker_info.FClassifyTag = 2  # 已完成
        elif action == '1':
            teamworker_info.FClassifyTag = 1  # 进行中
        else:
            self.response_data['result'] = '13'
            self.response_data['msg'] = 'ACTION只能传0或1'

            return False

        teamworker_info.FApproveMemo = approveMemo
        teamworker_info.FApproveDate = timezone.now()
        teamworker_info.save()

        teamworker_info = teamworker.objects.filter(Q(FID=teamworkerID))

        self.response_data['result'] = '0'
        self.response_data['msg'] = 'success'
        self.response_data['data'] = convert_to_dicts(teamworker_info)


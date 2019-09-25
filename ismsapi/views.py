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
from group.models import group
from personnel.models import personnel
from organize.models import organize
from basedata.models import base
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








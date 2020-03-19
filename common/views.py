from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from .models import sequence
from django.db.models import Q
from devinterface.models import devinterface, interfaceparam
from device.models import device, devcallinterface
from pedpassage.models import pedpassage
from project.models import project
import time
import base64
import hmac
import uuid
import json
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import urllib.parse
import urllib.request
import calendar
import requests
import re
import random
import string


# Create your views here.
from pytz import unicode


def json_field(field_data):
    """
    将字典的键值转化为对象
    :param field_data:
    :return:
    """
    if isinstance(field_data, str):
        return "\"" + field_data + "\""
    elif isinstance(field_data, bool):
        if field_data == 'False':
            return 'false'
        else:
            return 'true'
    elif isinstance(field_data, unicode):
        return "\"" + field_data.encode('utf-8') + "\""
    elif field_data is None:
        return "\"\""
    else:
        return "\"" + str(field_data) + "\""


def json_encode_dict(dict_data):
    """
    将字典转化为json序列
    :param dict_data:
    :return:
    """
    json_data = "{"
    for (k, v) in dict_data.items():
        json_data = json_data + json_field(k) + ':' + json_field(v) + ', '
    json_data = json_data[:-2] + "}"
    return json_data


def json_encode_list(list_data):

    """
    将列表中的字典元素转化为对象
    :param list_data:
    :return:
    """
    json_res = "["
    for item in list_data:
        json_res = json_res + json_encode_dict(item) + ", "
    return json_res[:-2] + "]"


def objects_to_json(objects, model):

    """
    将 model对象 转化成 json
        example：
            1. objects_to_json(Test.objects.get(test_id=1), EviewsUser)
            2. objects_to_json(Test.objects.all(), EviewsUser)
    :param objects: 已经调用all 或者 get 方法的对象
    :param model: objects的 数据库模型类
    :return:
    """
    from collections import Iterable
    concrete_model = model._meta.concrete_model
    list_data = []

    # 处理不可迭代的 get 方法
    if not isinstance(object, Iterable):
        objects = [objects, ]

    for obj in objects:
        dict_data = {}
        print(concrete_model._meta.local_fields)
        for field in concrete_model._meta.local_fields:
            if field.name == 'user_id':
                continue
            value = field.value_from_object(obj)
            dict_data[field.name] = value
        list_data.append(dict_data)

    data = json_encode_list(list_data)
    return data


def json_to_objects(json_str, model):

    """
    将 将反序列化的json 转为 model 对象
        example:
            Test model 预先定义
            test_str = '[{"test_id":"0", "test_text":"hello json_to_objects"}]'
            json_to_objects(json_str, model)
    :param json_str:
    :param model: objects的 数据库模型类
    :return:
    """
    import ast
    json_list = ast.literal_eval(json_str)
    obj_list = []
    field_key_list = [field.name for field in model._meta.concrete_model._meta.local_fields]
    for item in json_list:
        obj = model()
        for field in item:
            if field not in field_key_list:
                raise ValueError('数据库无 ' + field + ' 字段')
            setattr(obj, field, item[field])
        obj_list.append(obj)
    return obj_list


def convert_to_dicts(objs):
    """
    将Queryset 数据集 字典化
    :param objs: Queryset 数据集
    :return: 字典数组
    """
    obj_arr=[]

    for o in objs:
        dict = {}
        dict.update(o.__dict__)
        dict.pop("model", None)
        dict.pop("_state", None)
        dict.pop("pk", None)
        dict['FID_Split'] = ''.join(str(o.FID).split('-'))

        obj_arr.append(dict)
    return obj_arr

#根据当前时间戳显示时间格式
def getDateTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


#产生token
def generate_token(key, expire=3600):
    """
        创建产生token
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    """
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))

    return b64_token.decode("utf-8")

#校验token
def certify_token(key, token):
    """
        验证token
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    """
    response_data = {}
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            response_data['result'] = '3'
            response_data['msg'] = 'args illegal'

            return response_data
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            # token 过期
            response_data['result'] = '1'
            response_data['msg'] = 'token has expired'

            return response_data
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # token 验证失败
            response_data['result'] = '2'
            response_data['msg'] = 'token validation failed'

            return response_data
        # token 验证成功
        response_data['result'] = '0'
        response_data['msg'] = 'token validation success'

        return response_data
    except:
        response_data['result'] = '2'
        response_data['msg'] = 'token validation failed'

        return response_data

#生成uuid
def generate_uuid(request):
    struuid = ''.join(str(uuid.uuid1()).split('-'))

    return HttpResponse(struuid)

#生成md5校验
def generate_md5(request):
    if request.method == 'GET':
        appkey = request.GET.get('appkey')
        strkey = appkey + 'hm100'

        md_5 = hashlib.md5()
        md_5.update(strkey.encode("utf8"))

        sign = md_5.hexdigest()

        return HttpResponse(sign)

#生成下拉列表字典对象
def get_dict_object(request, model, fid, fname):
    r = [("", '请选择数据')]
    for obj in model:

        uuid = getattr(obj, fid)
        suuid = ''.join(str(uuid).split('-'))

        r = r + [(suuid, getattr(obj, fname))]
    return r

def get_dict_table(model, fid, fname):
    dict_type = []

    for obj in model:
        dict = {}

        uuid = getattr(obj, fid)
        suuid = ''.join(str(uuid).split('-'))

        dict['id'] = suuid
        dict['name'] = getattr(obj, fname)

        dict_type.append(dict)

    dictdata = json.dumps(dict_type)
    return dictdata

#判断日期格式是否有效
def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def get_dict_transfer(model, fid, fname, disabledfield):
    dict_transfer = []

    for obj in model:
        dict = {}

        uuid = getattr(obj, fid)
        suuid = ''.join(str(uuid).split('-'))

        dict['value'] = suuid
        dict['title'] = getattr(obj, fname)

        if getattr(obj, disabledfield) == False:
            dict['disabled'] = 'true'
        else:
            dict['disabled'] = ''

        dict_transfer.append(dict)

    return json.dumps(dict_transfer)


#判断项目编号session是否存在的装饰器
def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        #print('自定义装饰器被调用了')
        #print('请求路径%s' % request.path)
        prj_id = request.session.get('PrjID')

        if not prj_id:
            return redirect('/login/index/')

        return func(self, request, *args, **kwargs)
    return wrapper


#自动单据流水号生成
def gensequence(appname, prefix, zfill, type):

    try:
        sequence_info = sequence.objects.get(Q(FPrefix=appname))
        if type == 0:
            seq = sequence_info.FSequence
            if seq == None:
                seq = 1
            else:
                seq += 1
        else:
            tempdate = timezone.now().strftime('%Y-%m-%d')
            if str(sequence_info.FDate) != tempdate:
                seq = 1
            else:
                seq = sequence_info.FSequence + 1 
                
        n = str(seq).zfill(zfill)

        sequence_info.FDate = timezone.now().strftime('%Y-%m-%d')
        sequence_info.FSequence = seq
        sequence_info.save()
        
        return prefix + n
                    
    except ObjectDoesNotExist:
        
        seq = 1
        n = str(seq).zfill(zfill)

        sequence_info = sequence()
        sequence_info.FPrefix = appname
        sequence_info.FDate = timezone.now().strftime('%Y-%m-%d')
        sequence_info.FSequence = seq
        sequence_info.save()

        return prefix + n


#根据接口编号获取接口地址
def get_interface_url(interID):

    interface_info = devinterface.objects.get(Q(FID=interID))
    callinterface_info = devcallinterface.objects.filter(Q(FInterfaceID=interID)).first()
    if callinterface_info != None:
        inter_address = []
        dev_info = device.objects.filter(Q(FID=callinterface_info.FPID))
        for obj_dev in dev_info:
            if str(obj_dev.FDevIP) == '0.0.0.0':
                inter_address = interface_info.FAddress
            else:
                inter_address.append(str(obj_dev.FDevIP) + ':' + str(obj_dev.FPort) + interface_info.FAddress)
    else:
        # inter_address.append(interface_info.FAddress)
        inter_address = interface_info.FAddress
    return inter_address


#根据接口编号获取接口参数
def get_interface_param(interID):
    values = {}

    param_info = interfaceparam.objects.filter(Q(FPID=interID), Q(FPosition=0)).order_by('FSequence')
    interface_info = devinterface.objects.get(Q(FID=interID))

    for obj in param_info:
         if obj.FTypeID == '60504318e0cd11e9b62f7831c1d24216':
            data = obj.FValue
            return data
         else:
            values[obj.FParam] = obj.FValue

    #if interface_info.FRequestType == 0:
    data = urllib.parse.urlencode(values)
    #else:
    #    data = urllib.parse.urlencode(values).encode('utf-8')

    return data


#调用接口获得返回值
def get_interface_result(interID, paramsvalue=[], headersvalue=[], urlsvalue=[]):

    url = get_interface_url(interID)
    param = get_interface_param(interID)

    if len(paramsvalue) > 0:
        param = urllib.parse.unquote(param)
        key = re.findall(r"\$\{.*?\}", param)

        for i in range(len(key)):
            if len(key) == len(paramsvalue):
                param = param.replace(key[i], str(paramsvalue[i]))

        param = param.encode('utf-8')

    if len(urlsvalue) > 0:
        key = re.findall(r"\$\{.*?\}", url)

        for i in range(len(key)):
            url = url.replace(key[i], urlsvalue[i])

    interface_info = devinterface.objects.get(Q(FID=interID))

    if interface_info.FRequestType == 0:
        req = url + '?' + param

        response = urllib.request.urlopen(req)
        data = response.read()
        data = data.decode('utf-8')

        result = json.loads(data)

        return result
    elif interface_info.FRequestType == 1:
        header_param = interfaceparam.objects.filter(Q(FPID=interID), Q(FPosition=1)).order_by('FSequence')
        HEADERS = {}

        for hds in header_param:
            HEADERS[hds.FParam] = hds.FValue

        if len(headersvalue) > 0:
            headers = urllib.parse.urlencode(HEADERS)
            headers = urllib.parse.unquote(headers)

            key = re.findall(r"\$\{.*?\}", headers)

            for i in range(len(key)):
                if len(key) == len(headersvalue):
                    headers = headers.replace(key[i], headersvalue[i])

            HEADERS =  get_HEADER_json(urllib.parse.parse_qsl(headers))

        #HEADERS = {'Content-Type': 'application/json', 'token': '9422e6dcf4db405a975de8232930aada'}
        content = requests.post(url=url, headers=HEADERS, data=param, verify=False ).text
        #content.encoding = 'utf-8'

        content = json.loads(content)

        return content

#处理转换HEADER格式
def get_HEADER_json(headerlist):
    dict = {}

    for obj in headerlist:
        dict[obj[0]] = obj[1]

    return dict


#获取本月第一天和本月最后一天日期
def get_current_month_start_and_end(date):
    """
    年份 date(2017-09-08格式)
    :param date:
    :return:本月第一天日期和本月最后一天日期
    """
    #if date.count('-') != 2:
    #    raise ValueError('- is error')
    year, month = str(date).split('-')[0], str(date).split('-')[1]
    end = calendar.monthrange(int(year), int(month))[1]
    start_date = '%s-%s-01' % (year, month)
    end_date = '%s-%s-%s' % (year, month, end)
    return start_date, end_date


#生成一组数字加字母的随机字符串
def get_Random_String(n):
    string.printable=string.ascii_letters + string.digits
    x = string.printable
    salt = ''
    for i in range(n):
        salt+=random.choice(x)
    return salt


def getModelResult(model, *orders, **wheres):
    ret = model.objects

    ret = ret.filter(**wheres)

    for order in orders:
        ret = ret.order_by(order)

    return ret

#处理组织数据隔离
def org_split(queryset, request, **condtions):
    IsSplit = request.session['OrgIsSplit']
    Orgid = request.session['UserOrg']

    if IsSplit == True:
        if len(condtions) == 0:
            condtions = {"CREATED_ORG": Orgid}

        return queryset.filter(**condtions)

    return queryset


#处理原生sql转成字典
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

#根据项目返回管理组织
def prj_2_manageorg(prjID):
    try:
        if prjID == '':
            return ''
        else:
            prj_info = project.objects.get(Q(FID=prjID))
        return prj_info.FManageORG
    except ObjectDoesNotExist:
        return ''


#根据接口号返回设备ID
def intID_2_devID(initID):
    try:
        devcall_info = devcallinterface.objects.filter(Q(FInterfaceID=initID)).first()
        devcall_fpid = devcall_info.FPID

        dev_id = device.objects.get(Q(FID=devcall_fpid)).FDevID

        return dev_id
    except Exception as e:
        return str(e)


#根据设备号返回项目值
def deviceID_2_prjID(deviceID):
    deviceID = str(deviceID)

    try:
        device_info = device.objects.get(Q(FDevID=deviceID))

        return device_info.CREATED_PRJ
    except ObjectDoesNotExist:
        return ''


#根据设备返回项目区域
def deviceID_2_areaID(deviceID):
    try:
        rs = pedpassage.objects.get(Q(FDevID=deviceID))

        return rs.FAreaID
    except ObjectDoesNotExist:
        return  ''
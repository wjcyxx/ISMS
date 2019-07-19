from django.shortcuts import render
from django.shortcuts import HttpResponse
import time
import base64
import hmac
import uuid
import json
import hashlib

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

        obj_arr.append(dict)
    return obj_arr

def getDateTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


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


def generate_uuid(request):
    struuid = ''.join(str(uuid.uuid1()).split('-'))

    return HttpResponse(struuid)

def generate_md5(request):
    if request.method == 'GET':
        ukey = request.GET.get('ukey')
        strkey = ukey + 'brjNC100'

        md_5 = hashlib.md5()
        md_5.update(strkey.encode("utf8"))

        sign = md_5.hexdigest()

        return HttpResponse(sign)


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




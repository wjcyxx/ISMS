from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import *
from django.db.models import Q
from common.views import *
from django.http import JsonResponse
from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge

'''-------------------------------------------------------------------------------------------------
    字典类型管理
   -------------------------------------------------------------------------------------------------
'''
def basetype(request):
    return render(request, 'content/basetype/basetypeinfo.html')

def get_datasource(request):
    serinput = request.POST.get("resultdict[FBase]", '')

    Base_info = base.objects.filter(Q(FBase__contains=serinput), (Q(FPID__isnull=True)))

    dict = convert_to_dicts(Base_info)
    resultdict = {'code':0, 'msg':"", 'count': Base_info.count(), 'data': dict}

    return  JsonResponse(resultdict, safe=False)

def add(request):
    obj = BasetypeModelForm()

    return render(request, "content/basetype/basetypeadd.html", {'obj': obj})


def edit(request):
    fid = request.GET.get('fid')

    Base_info = base.objects.get(FID=fid)
    obj = BasetypeModelForm(instance=Base_info)

    return render(request, "content/basetype/basetypeedit.html", {'obj': obj})


def insert(request):
    if request.method == 'POST':
        obj = BasetypeModelForm(request.POST)

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

        Base_info = base.objects.get(FID=fid)
        obj = BasetypeModelForm(request.POST, instance=Base_info)

        if obj.is_valid():
            temp = obj.save(commit=False)
            temp.UPDATED_BY = request.session['UserID']

            temp.save()
            response_data['result'] = '0'
        else:
            response_data['msg'] = obj.errors
            response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))

def delete(request):
    if request.method == 'POST':

        response_data = {}
        fid = ''.join(str(request.POST.get('fid')).split('-'))

        num = base.objects.filter(Q(FPID=fid)).count()
        if num > 0:
            response_data['result'] = '2'
            return HttpResponse(json.dumps(response_data))

        try:
            base.objects.get(FID=fid).delete()
            response_data['result'] = '0'
        except:
            response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))

'''-------------------------------------------------------------------------------------------------
    数据字典管理
   -------------------------------------------------------------------------------------------------
'''
def basedata(request):
    dict_type = []

    Basetype = base.objects.filter(FPID__isnull=True)

    for bt in Basetype:
        dict = {}
        dict['id'] = ''.join(str(bt.FID).split('-'))
        dict['name'] = bt.FBase

        dict_type.append(dict)

    bdata = json.dumps(dict_type)

    return render(request, "content/basedata/basedatainfo.html", {'bdata': bdata})

def getbasedata_datasource(request):
    serinput = request.POST.get("resultdict[FBase]", '')
    page = request.POST.get('page')
    rows = request.POST.get('limit')

    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)

    Base_info = base.objects.filter(Q(FBase__contains=serinput), Q(FPID__isnull=False))
    total = Base_info.count()
    Base_info = Base_info[i:j]

    dict = convert_to_dicts(Base_info)
    resultdict = {'total':total, 'code':0, 'msg':"", 'count': total, 'data': dict}

    return  JsonResponse(resultdict, safe=False)


def get_object(request):
    r = [("", '请选择字典类型')]
    for obj in base.objects.filter(FPID__isnull=True):
       suuid = ''.join(str(obj.FID).split('-'))

       r = r + [(suuid, obj.FBase)]
    return r

def basedata_add(request):
    obj = BasedataModelForm()

    obj.fields['FPID'].choices = get_object(request)
    return render(request, "content/basedata/basedataadd.html", {'obj': obj})

def basedata_edit(request):
    fid = request.GET.get('fid')

    basedata_info = base.objects.get(FID=fid)
    obj = BasedataModelForm(instance=basedata_info)
    obj.fields['FPID'].choices = get_object(request)

    return render(request, "content/basedata/basedataedit.html", {'obj': obj})


def basedata_insert(request):
    if request.method == 'POST':

        response_data = {}

        obj = BasetypeModelForm(request.POST)

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

def basedata_update(request):
    if request.method == 'POST':

        response_data = {}
        dict={}

        fid = request.POST.get('FID')

        Base_info = base.objects.get(FID=fid)
        dict['CREATED_BY'] = Base_info.CREATED_BY
        dict['CREATED_TIME'] = Base_info.CREATED_TIME

        obj = BasedataModelForm(request.POST, instance=Base_info)
        obj.fields['FPID'].choices = get_object(request)

        if obj.is_valid():
            temp = obj.save(commit=False)
            temp.CREATED_BY = dict['CREATED_BY']
            temp.CREATED_TIME = dict['CREATED_TIME']

            temp.save()
            response_data['result'] = '0'
        else:
            response_data['msg'] = obj.errors
            response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))

def basedata_delete(request):
    if request.method == 'POST':

        response_data = {}
        fid = request.POST.get('fid')

        try:
            base.objects.get(FID=fid).delete()
            response_data['result'] = '0'
        except:
            response_data['result'] = '1'

        return HttpResponse(json.dumps(response_data))

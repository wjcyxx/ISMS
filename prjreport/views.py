from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from project.models import project
from common.views import *
from django.http import JsonResponse
#from .forms import *
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
# Create your views here.


#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/prjreport/prjreportinfo.html'


#返回table数据及查询结果
class get_datasource(get_datasource_base):
    def get_queryset(self, reqeust):
        Orgid = self.request.session['UserOrg']
        serinput = self.request.POST.get("resultdict[FPrjname]", '')
        condtions = {"FManageORG": Orgid}

        Project_info = project.objects.filter(Q(FPrjname__contains=serinput))
        Project_info.filter(**condtions)

        return Project_info

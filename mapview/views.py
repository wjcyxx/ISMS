from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import Q
from common.views import *
from project.models import project
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
# Create your views here.

#控制器入口
class entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/mapview/mapview.html'
        project_info = project.objects.all()

        self.context['projectinfo'] = project_info


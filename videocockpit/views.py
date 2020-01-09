from django.shortcuts import render
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q, Sum, Count
from basedata.models import base
from project.models import project
from device.models import device
from devinterfacesrv.models import envinterfacesrv
from common.views import *
from django.http import JsonResponse
from busmenu.models import busmenu
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
from django.db import connection
from django.db.models import Sum, Count
import re

# Create your views here.

class videocockpit_entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/datacockpit/videocockpit.html'

        busmenu_info = busmenu.objects.filter(Q(FPID__isnull=True) | Q(FPID=''), Q(FStatus=True), Q(FMenuPosition=2)).order_by('FSequence')
        self.context['busmenu_info'] = busmenu_info

from django.shortcuts import render
import urllib.parse
import urllib.request
import hmac
import base64
import hashlib
from hashlib import sha256
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.db.models import Q, Sum, Count
from basedata.models import base
from project.models import project
from devinterfacesrv.models import envinterfacesrv
from common.views import *
from django.http import JsonResponse
from busmenu.models import busmenu
from appkey.models import appkey
from monitordev.models import monitordev
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from baseframe.baseframe import *
import datetime
from django.db import connection
from django.db.models import Sum, Count
import re

class epidcockpit_entrance(EntranceView_base):
    def set_view(self, request):
        self.template_name = 'content/datacockpit/epidcockpit.html'

        busmenu_info = busmenu.objects.filter(Q(FPID__isnull=True) | Q(FPID=''), Q(FStatus=True), Q(FMenuPosition=2)).order_by('FSequence')
        self.context['busmenu_info'] = busmenu_info

        Orgid = self.request.session['UserOrg']
        project_info = project.objects.filter(Q(FStatus=True))
        condtions = {"FManageORG": Orgid}
        project_info = org_split(project_info, self.request, **condtions)

        self.context['projectinfo'] = project_info

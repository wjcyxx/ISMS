from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.db import models
from common.views import *
from django.http import JsonResponse
import json
from django.utils import timezone
from django.forms import widgets as Fwidge
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
# Create your views here.

#global req

class EntranceView(View):
    template_name = ''
    context = {}

    @login_decorator
    def get(self, request, *args):
        return render(self.request, self.template_name, self.context)

    def post(self, request):
        pass

class get_datasource(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):


        pass


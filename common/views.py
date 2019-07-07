from django.shortcuts import render
from django.shortcuts import HttpResponse
import uuid

# Create your views here.
def generate_uuid(request):
    struuid = ''.join(str(uuid.uuid1()).split('-'))

    return HttpResponse(struuid)
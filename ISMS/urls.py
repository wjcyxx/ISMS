"""ISMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login import views
from common.views import generate_uuid, get_interface_param, generate_md5
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls'), name='login'),
    path('organize/', include('organize.urls'), name='organize'),
    path('project/', include('project.urls'), name='project'),
    path('genuuid/', generate_uuid, name='genuuid'),
    path('genmd5/', generate_md5, name='genmd5'),
    path('get_interface_param/<str:interID>/', get_interface_param),
    path('basedata/', include('basedata.urls'), name='basedata'),
    path('user/', include('user.urls'), name='user'),
    path('area/', include('area.urls'), name='area'),
    path('projectmap/', include('projectmap.urls'), name='projectmap'),
    path('team/', include('team.urls'), name='team'),
    path('group/', include('group.urls'), name='group'),
    path('personnel/', include('personnel.urls'), name='personnel'),
    path('personauth/', include('personauth.urls'), name='personauth'),
    path('device/', include('device.urls'), name='device'),
    path('devinterface/', include('devinterface.urls'), name='devinterface'),
    path('pedpassage/', include('pedpassage.urls'), name='pedpassage'),
    path('passagerecord/', include('passagerecord.urls'), name='passagerecord'),
    path('hatrule/', include('hatrule.urls'), name='hatrule'),
    path('hatalertlog/', include('hatalertlog.urls'), name='hatalertlog'),
    path('safetrain/', include('safetrain.urls'), name='safetrain'),
    path('envdatalog/', include('envdatalog.urls'), name='envdatalog'),
    path('envrule/', include('envrule.urls'), name='envrule'),
    path('envalarmlog/', include('envalarmlog.urls'), name='envalarmlog'),
    path('vehiclegate/', include('vehiclegate.urls'), name='vehiclegate'),
    path('vehiclefiles/', include('vehiclefiles.urls'), name='vehiclefiles'),
    path('vehiclepasslog/', include('vehiclepasslog.urls'), name='vehiclepasslog'),
    path('elecfencle/', include('elecfencle.urls'), name='elecfencle'),
    path('elecalarm/', include('elecalarm.urls'), name='elecalarm'),
    path('goodstype/', include('goodstype.urls'), name='goodstype'),
    path('unit/', include('unit.urls'), name='unit'),
    path('materials/', include('materials.urls'), name='materials'),
    path('receaccount/', include('receaccount.urls'), name='receaccount'),
    path('recepound/', include('recepound.urls'), name='recepound'),
    path('issueaccount/', include('issueaccount.urls'), name='issueaccount'),
    path('issuepound/', include('issuepound.urls'), name='issuepound'),
    path('abnpound/', include('abnpound.urls'), name='abnpound'),
    path('menchanical/', include('menchanical.urls'), name='menchanical'),
    path('menccheck/', include('menccheck.urls'), name='menccheck'),
    path('mencrepairplan/', include('mencrepairplan.urls'), name='mencrepairplan'),
    path('mencrepairlog/', include('mencrepairlog.urls'), name='mencrepairlog'),
    path('monitordev/', include('monitordev.urls'), name='monitordev'),
    path('dsps/', include('dsps.urls'), name='dsps'),
    path('envdetection/', include('envdetection.urls'), name='envdetection'),
    path('personinfomap/', include('personinfomap.urls'), name='personinfomap'),
    path('mainanalyse/', include('mainanalyse.urls'), name='mainanalyse'),
    path('elevator/', include('elevator.urls'), name='elevator'),
    path('towercrane/', include('towercrane.urls'), name='towercrane'),
    path('mapview/', include('mapview.urls'), name='mapview'),
    path('visitor/', include('visitor.urls'), name='visitor'),
    path('usergroup/', include('usergroup.urls'), name='usergroup'),
    path('interface/', include('interface.urls'), name='interface'),
    path('unloading/', include('unloading.urls'), name='unloading'),
    path('busmenu/', include('busmenu.urls'), name='busmenu'),
    path('appkey/', include('appkey.urls'), name='appkey'),
    path('ismsapi/', include('ismsapi.urls'), name='ismsapi')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
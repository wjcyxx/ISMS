from django.urls import path
from . import views

app_name="datacockpit"

urlpatterns = [
    path('get_datacockpit/', views.get_datacockpit.as_view(), name='get_datacockpit'),
    path('get_prjcockpit/', views.get_prjcockpit.as_view(), name='get_prjcockpit'),
    path('get_prjstatus/', views.get_prjstatus.as_view(), name='get_prjstatus'),
    path('get_prjcost/', views.get_prjcost.as_view(), name='get_prjcost'),
    path('get_iotdev/', views.get_iotdev.as_view(), name='get_iotdev'),
    path('get_personregcount/', views.get_personregcount.as_view(), name='get_personregcount'),
    path('get_personquitcount/', views.get_personquitcount.as_view(), name='get_personquitcount'),
    path('get_personsitcount/', views.get_personsitcount.as_view(), name='get_personsitcount'),
    path('get_personauthcount/', views.get_personauthcount.as_view(), name='get_personauthcount'),
    path('get_citypm/', views.get_citypm.as_view(), name='get_citypm'),
    path('get_mapdata/', views.get_mapdata.as_view(), name='get_mapdata')
]

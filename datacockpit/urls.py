from django.urls import path
from . import views

app_name="datacockpit"

urlpatterns = [
    path('get_datacockpit/', views.get_datacockpit.as_view(), name='get_datacockpit'),
    path('get_prjcockpit/', views.get_prjcockpit.as_view(), name='get_prjcockpit'),
    path('get_prjstatus/', views.get_prjstatus.as_view(), name='get_prjstatus'),
    path('get_prjcost/', views.get_prjcost.as_view(), name='get_prjcost'),
    path('get_iotdev/', views.get_iotdev.as_view(), name='get_iotdev')
]

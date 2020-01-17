from django.urls import path
from . import views

app_name="videocockpit"

urlpatterns = [
    path('videocockpit_entrance/', views.videocockpit_entrance.as_view(), name='videocockpit_entrance'),
    path('get_videocount/', views.get_videocount.as_view(), name='get_videocount'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('get_videourl/', views.get_videourl.as_view(), name='get_videourl'),
    path('get_prjcount/', views.get_prjcount.as_view(), name='get_prjcount')
]
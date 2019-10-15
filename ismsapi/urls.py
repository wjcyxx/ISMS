from django.urls import path
from . import views

app_name="ismsapi"

urlpatterns = [
    path('get_token/', views.get_token.as_view(), name='get_token'),
    path('check_user/', views.check_user.as_view(), name='check_user'),
    path('get_project/', views.get_project.as_view(), name='get_project'),
    path('get_team/', views.get_team.as_view(), name='get_team'),
    path('get_orgainze/', views.get_orgainze.as_view(), name='get_orgainze'),
    path('get_basedate/', views.get_basedate.as_view(), name='get_basedate'),
    path('get_group/', views.get_group.as_view(), name='get_group'),
    path('get_personnel/', views.get_personnel.as_view(), name='get_personnel'),
    path('get_pedpassage/', views.get_pedpassage.as_view(), name='get_pedpassage'),
    path('get_passagerecord/', views.get_passagerecord.as_view(), name='get_passagerecord')

]
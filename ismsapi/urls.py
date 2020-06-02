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
    path('get_passagerecord/', views.get_passagerecord.as_view(), name='get_passagerecord'),
    path('get_env_realdata/', views.get_env_realdata.as_view(), name='get_env_realdata'),
    path('create_prjcheck/', views.create_prjcheck.as_view(), name='create_prjcheck'),
    path('get_prjcheck/', views.get_prjcheck.as_view(), name='get_prjcheck'),
    path('get_env_hisdata/', views.get_env_hisdata.as_view(), name='get_env_hisdata'),
    path('delete_prjcheck/', views.delete_prjcheck.as_view(), name='delete_prjcheck'),
    path('create_prjcheck_pic/', views.create_prjcheck_pic.as_view(), name='create_prjcheck_pic'),
    path('get_prjcheck_pic/', views.get_prjcheck_pic.as_view(), name='get_prjcheck_pic'),
    path('delete_prjcheck_pic/', views.delete_prjcheck_pic.as_view(), name='delete_prjcheck_pic'),
    path('get_elevator_hisdata/', views.get_elevator_hisdata.as_view(), name='get_elevator_hisdata'),
    path('get_menchanical/', views.get_menchanical.as_view(), name='get_menchanical'),
    path('get_recepound/', views.get_recepound.as_view(), name='get_recepound'),
    path('get_recepound_goodsDetail/', views.get_recepound_goodsDetail.as_view(), name='get_recepound_goodsDetail'),
    path('get_vehiclepasslog/', views.get_vehiclepasslog.as_view(), name='get_vehiclepasslog'),
    path('get_vehiclegate/', views.get_vehiclegate.as_view(), name='get_vehiclegate'),
    path('modify_user_loginpwd/', views.modify_user_loginpwd.as_view(), name='modify_user_loginpwd'),
    path('create_filefolder/', views.create_filefolder.as_view(), name='create_filefolder'),
    path('modify_filefolder/', views.modify_filefolder.as_view(), name='modify_filefolder'),
    path('get_filefolder/', views.get_filefolder.as_view(), name='get_filefolder'),
    path('delete_filefolder/', views.delete_filefolder.as_view(), name='delete_filefolder'),
    path('upload_file/', views.upload_file.as_view(), name='upload_file'),
    path('get_folder_infiles/', views.get_folder_infiles.as_view(), name='get_folder_infiles'),
    path('delete_files/', views.delete_files.as_view(), name='delete_files')
]
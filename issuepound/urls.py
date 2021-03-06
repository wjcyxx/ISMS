from django.urls import path
from . import views

app_name="issuepound"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('get_originbill_datasource/', views.get_originbill_datasource.as_view(), name='get_originbill_datasource'),
    path('get_material_datasource/', views.get_material_datasource.as_view(), name='get_material_datasource'),
    path('recevoid/', views.recevoid.as_view(), name='recevoid'),
    path('get_unitid/', views.get_unitid.as_view(), name='get_unitid'),
    path('show_originupload/', views.show_originupload.as_view(), name='show_originupload')
]
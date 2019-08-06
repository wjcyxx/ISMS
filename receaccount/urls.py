from django.urls import path
from . import views

app_name="receaccount"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('get_originbill_datasource/', views.get_originbill_datasource.as_view(), name='get_originbill_datasource')
]
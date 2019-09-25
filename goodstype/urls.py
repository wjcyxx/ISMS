from django.urls import path
from . import views

app_name="goodstype"

urlpatterns = [
    path('entrance/', views.entrance.as_view(), name='entrance'),
    path('get_datasource/', views.get_datasource.as_view(), name='get_datasource'),
    path('add/', views.add.as_view(), name='add'),
    path('edit/', views.edit.as_view(), name='edit'),
    path('insert/', views.insert.as_view(), name='insert'),
    path('delete/', views.delete.as_view(), name='delete'),

    path('add_subtype/', views.add_subtype.as_view(), name='add_subtype'),
    path('get_subtype_datasource/', views.get_subtype_datasource.as_view(), name='get_subtype_datasource'),
    path('insert_subtype/', views.insert_subtype.as_view(), name='insert_subtype'),
    path('delete_subtype/', views.delete_subtype.as_view(), name='delete_subtype'),
]
from django.urls import path
from . import views

app_name="projectmap"

urlpatterns = [
    path('projectmap/', views.projectmap, name='projectmap'),
    path('get_datasource/', views.get_datasource, name='get_datasource'),
    path('prjmap_upload/', views.prjmap_upload, name='prjmap_upload'),
    path('delete/', views.delete, name='delete')
]

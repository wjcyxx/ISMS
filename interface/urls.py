from django.urls import path
from . import views

app_name="interface"

urlpatterns = [
    path('passagedev_callback/', views.passagedev_callback.as_view(), name='passagedev_callback'),
    #path('base64_savepic/', views.base64_savepic, name='base64_savepic')


]
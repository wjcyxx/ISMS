"""ISMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login import views
from common.views import generate_uuid
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls'), name='login'),
    path('organize/', include('organize.urls'), name='organize'),
    path('project/', include('project.urls'), name='project'),
    path('genuuid/', generate_uuid, name='genuuid'),
    path('basedata/', include('basedata.urls'), name='basedata'),
    path('user/', include('user.urls'), name='user'),
    path('area/', include('area.urls'), name='area')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
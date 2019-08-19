from django.db import models
import uuid
from menchanical.models import menchanical
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class dsps(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMonitor = models.CharField(max_length=32, verbose_name='测点名称', blank=True, null=True)
    FMonitortypeID = models.CharField(max_length=32, verbose_name='测点类型', blank=True, null=True)
    FDevID = models.CharField(max_length=32, verbose_name='测量终端', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MonitorPoint'

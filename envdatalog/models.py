from django.db import models
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class envdatalog(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FDevID = models.CharField(max_length=32, verbose_name='设备ID', blank=True, null=True)
    FNodename = models.CharField(max_length=32, verbose_name='节点名称', blank=True, null=True)
    FMonitoritem1 = models.CharField(max_length=32, verbose_name='监测内容(一)', blank=True, null=True)
    FMonitorvalue1 = models.CharField(max_length=32, verbose_name='监测值(一)', blank=True, null=True)
    FMonitoritem2 = models.CharField(max_length=32, verbose_name='监测内容(二)', blank=True, null=True)
    FMonitorvalue2 = models.CharField(max_length=32, verbose_name='监测值(二)', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_EnvDataLog'

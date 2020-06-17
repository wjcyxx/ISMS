from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

# 任务列表模型
class tasklist(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FDevID = models.CharField(max_length=32, verbose_name='设备ID', blank=True, null=True)
    FChannelNo = models.IntegerField(verbose_name='摄像头通道号', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_TaskList'
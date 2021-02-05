from django.db import models
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class envrule(models.Model):

    COND_CHOICES = (
        (None, '请选择数据'),
        (0, '等于'),
        (1, '大于'),
        (2, '小于'),
        (3, '大于等于'),
        (4, '小于等于'),
        (5, '不等于')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FRule = models.CharField(max_length=32, verbose_name='规则名称', blank=True, null=True)
    FDevID = models.CharField(max_length=32, verbose_name='设备ID', blank=True, null=True)
    FAreaID = models.CharField(max_length=32, verbose_name='区域ID', blank=True, null=True)
    FNodename = models.CharField(max_length=32, verbose_name='节点名称', blank=True, null=True)
    FMonitoritem = models.CharField(max_length=32, verbose_name='监测项目', blank=True, null=True)
    FMonitorvalue = models.CharField(max_length=32, verbose_name='监测值', blank=True, null=True)
    FMonitorcondition = models.IntegerField(choices=COND_CHOICES, verbose_name='监测条件', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_EnvRule'


class envruleswitch(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, verbose_name='FPID', blank=True, null=True)
    FPort = models.IntegerField(verbose_name='继电器端口号', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='继电器状态')
    FCommand = models.CharField(max_length=32, verbose_name='继电器指令', blank=True, null=True)
    FDriverdevice = models.CharField(max_length=32, verbose_name='控制外设', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_EnvRuleSwitch'

from django.db import models
import uuid
from envrule.models import *
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class envalarmlog(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FRuleID = models.ForeignKey(envrule, to_field='FID', on_delete=models.CASCADE, verbose_name='触发规则ID', blank=True, null=True)
    FPortID = models.ForeignKey(envruleswitch, to_field='FID', on_delete=models.CASCADE, verbose_name='端口号ID', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_EnvAlarmLog'

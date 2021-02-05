from django.db import models
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class appkey(models.Model):
    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '内部应用'),
        (1, '外部应用')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FAppID = models.CharField(max_length=50, verbose_name='appkey', blank=True, null=True)
    FAppkey = models.CharField(max_length=50, verbose_name='appkey', blank=True, null=True)
    FAppSecret = models.CharField(max_length=50, verbose_name='appkey', blank=True, null=True)
    FAppName = models.CharField(max_length=50, verbose_name='应用名称', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FAppCreateTime = models.DateTimeField(verbose_name='app创建时间', blank=True, null=True)
    FType = models.IntegerField(choices=TYPE_CHOICES, verbose_name='APP类型', default=0, blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_AppKey'
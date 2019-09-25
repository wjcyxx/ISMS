from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class unit(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FUnit = models.CharField(max_length=32, verbose_name='计量单位名称', blank=True, null=True)
    FUnitgroupID = models.CharField(max_length=32, verbose_name='计量单位组', blank=True, null=True)
    FIsBaseunit = models.BooleanField(verbose_name='是否基准单位', default=False, blank=True, null=True)
    FConversion = models.FloatField(verbose_name='换算关系', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Unit'
        ordering = ['FUnitgroupID', '-FIsBaseunit', 'FUnit']

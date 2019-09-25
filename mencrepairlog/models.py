from django.db import models
import uuid
from menchanical.models import menchanical
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class mencrepairlog(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMecserialFID = models.ForeignKey(menchanical, to_field='FID', on_delete=models.CASCADE, blank=True, null=True)
    FSubmitter = models.CharField(max_length=32, verbose_name='故障提交人', blank=True, null=True)
    FSubmitdate = models.DateField(verbose_name='提交日期', blank=True, null=True)
    FHappendate = models.DateTimeField(verbose_name='故障发生时间', blank=True, null=True)
    FSite = models.CharField(max_length=32, verbose_name='发生部位', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MencRepairLog'

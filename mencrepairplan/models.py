from django.db import models
import uuid
from menchanical.models import menchanical
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class mencrepairplan(models.Model):

    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '固定频率'),
        (1, '随机抽查')
    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMecserialFID = models.ForeignKey(menchanical, to_field='FID', on_delete=models.CASCADE, blank=True, null=True)
    FChecktype = models.IntegerField(choices=TYPE_CHOICES, verbose_name='检查类型', blank=True, null=True)
    FInterval = models.IntegerField(verbose_name='固定频率时间', blank=True, null=True)
    FFirstcheckdate = models.DateField(verbose_name='首次检查日期', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MencRepairPlan'
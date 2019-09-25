from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class elecalarm(models.Model):

    TYPE_CHOICES = (
        (0, '进入围栏'),
        (1, '离开围栏')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FElecFenceID = models.CharField(max_length=32, verbose_name='围栏ID', blank=True, null=True)
    FPlate = models.CharField(max_length=32, verbose_name='报警对象', blank=True, null=True)
    FTriggerType = models.IntegerField(choices=TYPE_CHOICES, verbose_name='触发动作', blank=True, null=True)
    FTriggerlong = models.FloatField(verbose_name='触发坐标经度', blank=True, null=True)
    FTriggerlat = models.FloatField(verbose_name='触发坐标纬度', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_ElecAlarm'

from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class elecfencle(models.Model):

    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '所有车辆'),
        (1, '选定车辆')
    )

    COORD_CHOICES = (
        (0, '百度经纬度'),
        (1, 'GPS经纬度'),
        (2, '国测局经纬度')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FElecFence = models.CharField(max_length=32, verbose_name='围栏名称', blank=True, null=True)
    FMonitortype = models.IntegerField(choices=TYPE_CHOICES, verbose_name='监控方式', blank=True, null=True)
    FPlate = models.CharField(max_length=32, verbose_name='监控车牌', blank=True, null=True)
    FElecFenceCoordinate = models.CharField(max_length=1024, verbose_name='围栏坐标', blank=True, null=True)
    FDeviation = models.FloatField(verbose_name='报警偏离距离', blank=True, null=True)
    FCoordinatetype = models.IntegerField(choices=COORD_CHOICES, default=0, verbose_name='坐标类型')
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_ElecFencle'

from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class vehiclefiles(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPlate = models.CharField(max_length=32, unique=True, verbose_name='车牌号码', default='')
    FDrivers = models.CharField(max_length=32, verbose_name='驾驶人', blank=True, null=True)
    FOrgID = models.CharField(max_length=32, verbose_name='所属单位', blank=True, null=True)
    FVehicletypeID = models.CharField(max_length=32, verbose_name='车辆类型', blank=True, null=True)
    FValiddate = models.DateField(verbose_name='有效日期', blank=True, null=True)
    FMaterielID = models.CharField(max_length=32, verbose_name='运输物料', blank=True, null=True)
    FRfidcard = models.CharField(max_length=32, verbose_name='RFID卡号', blank=True, null=True)
    FDevID = models.CharField(max_length=32, verbose_name='GPS设备ID', blank=True, null=True)
    FIsMonitor = models.BooleanField(default=False, verbose_name='是否电子围栏监控')
    FTare = models.FloatField(verbose_name='车辆皮重', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_VehicleFiles'
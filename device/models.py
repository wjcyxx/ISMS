from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class device(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FDevID = models.CharField(max_length=32, verbose_name='设备编号', blank=True, null=True)
    FDevice = models.CharField(max_length=32, verbose_name='设备名称', blank=True, null=True)
    FDevtypeID = models.CharField(max_length=32, verbose_name='设备类型', blank=True, null=True)
    FDevIP = models.GenericIPAddressField(verbose_name='设备IP', blank=True, null=True)
    FPort = models.IntegerField(verbose_name='设备端口号', blank=True, null=True)
    FPosition = models.CharField(max_length=128, verbose_name='摆放位置', blank=True, null=True)
    FLong = models.FloatField(verbose_name='经度', blank=True, null=True)
    FLat = models.FloatField(verbose_name='经度', blank=True, null=True)
    FManufacturer = models.IntegerField(verbose_name='设备厂商', blank=True, null=True)
    FBrand = models.CharField(max_length=32, verbose_name='设备品牌', blank=True, null=True)
    FMainstaff = models.CharField(max_length=32, verbose_name='维护人员', blank=True, null=True)
    FMainstafftel = models.CharField(max_length=32, verbose_name='联系方式', blank=True, null=True)
    FWarrantyDate = models.DateField(verbose_name='质保期', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Device'
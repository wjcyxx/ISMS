from django.db import models
import uuid
from vehiclegate.models import vehiclegate
from vehiclefiles.models import vehiclefiles
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class vehiclepasslog(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FGateID = models.ForeignKey(vehiclegate, to_field='FID', on_delete=models.CASCADE, verbose_name='通道ID', blank=True, null=True)
    #FPlate = models.ForeignKey(vehiclefiles, to_field='FPlate', on_delete=models.CASCADE, verbose_name='车牌号码', blank=True, null=True)
    FPlate = models.CharField(max_length=10, verbose_name='车牌号码', blank=True, null=True)
    FPicturepath = models.ImageField(upload_to='Plate/', default='', verbose_name='抓拍图片', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_VehiclePassLog'
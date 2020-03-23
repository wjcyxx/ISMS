from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class materials(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMaterID = models.CharField(max_length=32, verbose_name='物料编码', blank=True, null=True)
    FName = models.CharField(max_length=32, verbose_name='物料名称', blank=True, null=True)
    FGoodsTypeID = models.CharField(max_length=32, verbose_name='物料类型编号', blank=True, null=True)
    FUnitID = models.CharField(max_length=32, verbose_name='计量单位', blank=True, null=True)
    FSpec = models.CharField(max_length=32, verbose_name='规格型号', blank=True, null=True)
    FTexture = models.CharField(max_length=32, verbose_name='材质', blank=True, null=True)
    FPositiveDeviation = models.FloatField(verbose_name='正偏差', blank=True, null=True)
    FNegativeDeviation = models.FloatField(verbose_name='负偏差', blank=True, null=True)
    FRFID = models.CharField(max_length=32, verbose_name='RFID', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='描述', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Materials'

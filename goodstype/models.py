from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class goodstype(models.Model):

    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '比例偏差'),
        (1, '范围偏差')
    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FGoodsTypeID = models.CharField(max_length=32, verbose_name='物料类型编号', blank=True, null=True)
    FGoodsType = models.CharField(max_length=32, verbose_name='物料类型', blank=True, null=True)
    FDeviationType = models.IntegerField(choices=TYPE_CHOICES, verbose_name='偏差类别', blank=True, null=True)
    FPositiveDeviation = models.FloatField(verbose_name='正偏差', blank=True, null=True)
    FNegativeDeviation = models.FloatField(verbose_name='负偏差', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='描述', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_GoodsType'
        ordering = ['FPID']

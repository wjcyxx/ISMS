from django.db import models
import uuid
from materials.models import materials
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class materialsaccount(models.Model):

    RECETYPE_CHOICES = (
        (0, '收料'),
        (1, '发料')
    )

    SOURCE_CHOICES = (
        (None, '请选择数据'),
        (0, '称重'),
        (1, '补录'),
        (2, '验收'),
        (3, '作废'),
        (4, '退回')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPoundNo = models.CharField(max_length=32, verbose_name='磅单编号', blank=True, null=True)
    FReceivetype = models.IntegerField(choices=RECETYPE_CHOICES, verbose_name='收发类型', blank=True, null=True)
    F1stWeighTime = models.DateTimeField(verbose_name='第一次称重时间', blank=True, null=True)
    F2ndWeighTime = models.DateTimeField(verbose_name='第二次称重时间', blank=True, null=True)
    F1stWeigh = models.FloatField(verbose_name='第一次称重重量', blank=True, null=True)
    F2ndWeigh = models.FloatField(verbose_name='第二次称重重量', blank=True, null=True)
    FWeighPerson = models.CharField(max_length=32, verbose_name='过磅员', blank=True, null=True)
    FStatus = models.IntegerField(choices=SOURCE_CHOICES, verbose_name='单据状态', blank=True, null=True)
    FOperationalOrgID = models.CharField(max_length=32, verbose_name='业务发生单位', blank=True, null=True)
    FPlate = models.CharField(max_length=32, verbose_name='车牌号码', blank=True, null=True)
    FWorktypeID = models.CharField(max_length=32, verbose_name='业务类型', blank=True, null=True)
    FWarehouseID = models.CharField(max_length=32, verbose_name='库房', blank=True, null=True)
    FUsesite = models.CharField(max_length=32, verbose_name='使用部位', blank=True, null=True)
    FWaybillNo = models.CharField(max_length=32, verbose_name='原始运单号', blank=True, null=True)
    FWaybillDate = models.DateField(verbose_name='单据日期', blank=True, null=True)
    FWaybillPicpath = models.ImageField(upload_to='material/', default='', verbose_name='运单图片', blank=True, null=True)
    FInPicpath1 = models.ImageField(upload_to='material/', default='', verbose_name='进场图片1', blank=True, null=True)
    FInPicpath2 = models.ImageField(upload_to='material/', default='', verbose_name='进场图片2', blank=True, null=True)
    FOutPicpath1 = models.ImageField(upload_to='material/', default='', verbose_name='出场图片2', blank=True, null=True)
    FOutPicpath2 = models.ImageField(upload_to='material/', default='', verbose_name='出场图片2', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='描述', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MaterialsAccount'


class materaccountgoods(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.ForeignKey(materialsaccount, to_field='FID', on_delete=models.CASCADE, blank=True, null=True)
    #FPID = models.CharField(max_length=32, verbose_name='FPID', blank=True, null=True)
    #FMaterID = models.CharField(max_length=32, verbose_name='物料编码', blank=True, null=True)
    FMaterID = models.ForeignKey(materials, to_field='FID', on_delete=models.CASCADE, blank=True, null=True)
    FWaybillQty = models.FloatField(verbose_name='运单数量', blank=True, null=True)
    FUnitID = models.CharField(max_length=32, verbose_name='计量单位', blank=True, null=True)
    FConfirmQty = models.FloatField(verbose_name='确认数量', blank=True, null=True)
    FDeviationQty = models.FloatField(verbose_name='偏差', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MaterialsAccountGoods'
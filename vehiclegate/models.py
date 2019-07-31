from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class vehiclegate(models.Model):

    GATETYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '入口'),
        (1, '出口')
    )

    ATTR_CHOICES = (
        (0, '普通通道'),
        (1, '货运称重通道')
    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FGate = models.CharField(max_length=32, verbose_name='通道名称', blank=True, null=True)
    FDevID = models.CharField(max_length=32, verbose_name='设备ID', blank=True, null=True)
    FAreaID = models.CharField(max_length=32, verbose_name='区域ID', blank=True, null=True)
    FGatetype = models.IntegerField(choices=GATETYPE_CHOICES, verbose_name='通道类型', blank=True, null=True)
    FGateattr = models.IntegerField(choices=ATTR_CHOICES, default=0, verbose_name='通道属性')
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_VehicleGate'

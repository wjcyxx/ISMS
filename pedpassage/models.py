from django.db import models
from personnel.models import personnel
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class pedpassage(models.Model):

    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '入口'),
        (1, '出口')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPassage = models.CharField(max_length=32, verbose_name='通道名称', blank=True, null=True)
    FDevID = models.CharField(max_length=32, verbose_name='设备编号', blank=True, null=True)
    FAreaID = models.CharField(max_length=32, verbose_name='区域编号', blank=True, null=True)
    FType = models.IntegerField(choices=TYPE_CHOICES, verbose_name='通道类型', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FInitStatus = models.BooleanField(default=False, verbose_name='初始化状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_PedPassage'


class passagerecord(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPersonID = models.ForeignKey(personnel, to_field='FID', on_delete=models.CASCADE, blank=True, null=True, verbose_name='人员ID')
    #FPersonID = models.CharField(max_length=32, verbose_name='人员ID', blank=True, null=True)
    #FPassageID = models.CharField(max_length=32, verbose_name='人行通道ID', blank=True, null=True)
    FPassageID = models.ForeignKey(pedpassage, to_field='FID', on_delete=models.CASCADE, blank=True, null=True, verbose_name='人行通道ID')
    FAuthtypeID = models.CharField(max_length=32, verbose_name='通行授权方式', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_PassageRecord'
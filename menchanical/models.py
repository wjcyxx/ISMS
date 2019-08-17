from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class menchanical(models.Model):

    SOURCE_CHOICES = (
        (None, '请选择数据'),
        (0, '自有'),
        (1, '租赁')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMecserialID = models.CharField(max_length=32, verbose_name='机械唯一编码', blank=True, null=True)
    FMectypeID = models.CharField(max_length=32, verbose_name='机械类型', blank=True, null=True)
    FMecspec = models.CharField(max_length=32, verbose_name='机械型号', blank=True, null=True)
    FMecsource = models.IntegerField(choices=SOURCE_CHOICES, verbose_name='机械来源', blank=True, null=True)
    FOwnerOrg = models.CharField(max_length=100, verbose_name='产权单位', blank=True, null=True)
    FRecordNo = models.CharField(max_length=100, verbose_name='产权备案号', blank=True, null=True)
    FRecorddate = models.DateField(verbose_name='备案日期', blank=True, null=True)
    FLease = models.CharField(max_length=32, verbose_name='机械租赁单位', blank=True, null=True)
    FManufacturer = models.CharField(max_length=32, verbose_name='生产厂商', blank=True, null=True)
    FProducdate = models.DateField(verbose_name='出厂日期', blank=True, null=True)
    FProducNo = models.CharField(max_length=32, verbose_name='出厂编号', blank=True, null=True)
    FMonitordevID = models.CharField(max_length=32, verbose_name='监控设备ID', blank=True, null=True)
    FMecmanager = models.CharField(max_length=32, verbose_name='机械管理员', blank=True, null=True)
    FMecmanagertel = models.CharField(max_length=32, verbose_name='联系方式', blank=True, null=True)
    FParameter = models.CharField(max_length=32, verbose_name='机械参数', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Menchanical'



class mecoperauth(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FAuthpersonID = models.CharField(max_length=32, verbose_name='授权操作人员ID', blank=True, null=True)
    FAuthTimeslot = models.CharField(max_length=32, verbose_name='授权操作时间段', blank=True, null=True)
    FAuthDeadline = models.CharField(max_length=32, verbose_name='截止日期', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MecOperAuth'

class mecoperlog(models.Model):

    BEH_CHOICES = (
        (None, '请选择数据'),
        (0, '上班'),
        (1, '下班')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMecserialFID = models.CharField(max_length=32, blank=True, null=True)
    FPersonID = models.CharField(max_length=32, verbose_name='操作人员', blank=True, null=True)
    FOperbeh = models.IntegerField(choices=BEH_CHOICES, verbose_name='操作行为', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MecOperLog'
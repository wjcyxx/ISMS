from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class devinterface(models.Model):
    TRANSMODE_CHOICES = (
        (None, '请选择数据'),
        (0, '实时'),
        (1, '间隔'),
        (2, '单次')
    )

    REQUEST_CHOICES = (
        (None, '请选择数据'),
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE')
    )

    SCOPE_CHOICES = (
        (None, '请选择数据'),
        (0, '项目'),
        (1, '组织'),
        (2, '全局')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FName = models.CharField(max_length=32, verbose_name='接口名称', blank=True, null=True)
    FInterfaceTypeID = models.CharField(max_length=32, verbose_name='接口方式', blank=True, null=True)
    FRequestType = models.IntegerField(choices=REQUEST_CHOICES, verbose_name='接口类型', blank=True, null=True)
    FTransmode = models.IntegerField(choices=TRANSMODE_CHOICES, verbose_name='传输方式', blank=True, null=True)
    FPort = models.IntegerField(verbose_name='设备端口号', blank=True, null=True)
    FInterval = models.IntegerField(verbose_name='间隔时间', blank=True, null=True)
    FAddress = models.CharField(max_length=1000, verbose_name='访问地址', blank=True, null=True)
    FAppFID = models.CharField(max_length=32, verbose_name='调用AppID', blank=True, null=True)
    FDevID = models.CharField(max_length=32, verbose_name='绑定设备', blank=True, null=True)           #已废弃
    FInterfaceExtID = models.CharField(max_length=32, verbose_name='扩展分类', blank=True, null=True)  #已废弃
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FSrvStatus = models.BooleanField(default=False, verbose_name='服务状态')
    FSrvFile = models.CharField(max_length=100, verbose_name='服务文件', blank=True, null=True)
    FSrvPID = models.IntegerField(verbose_name='服务文件PID', blank=True, null=True, default=0)
    FScope = models.IntegerField(choices=SCOPE_CHOICES, verbose_name='适配范围', blank=True, null=True, default=0)
    FCallSigCode = models.CharField(max_length=32, verbose_name='调用特征码', blank=True, null=True, unique=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_DevInterface'
        ordering = ['FDevID']


class interfaceparam(models.Model):

    POSITION_CHOICES = (
        (None, '请选择数据'),
        (0, 'BODY'),
        (1, 'HEADER')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FSequence = models.IntegerField(verbose_name='顺序号', default=0, blank=True, null=True)
    FParam = models.CharField(max_length=32, verbose_name='参数名称', blank=True, null=True)
    FValue = models.CharField(max_length=128, verbose_name='参数值', blank=True, null=True)
    FPosition = models.IntegerField(choices=POSITION_CHOICES, default=0, verbose_name='参数位置', blank=True, null=True)
    FTypeID = models.CharField(max_length=32, verbose_name='参数类型', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        db_table = 'T_InterfaceParam'

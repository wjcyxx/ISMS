from django.db import models
import uuid
from menchanical.models import menchanical
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class monitordev(models.Model):

    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '枪机'),
        (1, '球机')
    )

    PROTOCOL_CHOICES = (
        (None, '请选择数据'),
        (0, 'RTSP'),
        (1, 'ONVIF')
    )

    TRANSMODE_CHOICES = (
        (None, '请选择数据'),
        (0, 'TCP'),
        (1, 'UDP')
    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FDevID = models.CharField(max_length=32, verbose_name='设备唯一编码', blank=True, null=True)
    FChannel = models.CharField(max_length=32, verbose_name='通道名称', blank=True, null=True)
    FIPAddress = models.GenericIPAddressField(protocol='ipv4', verbose_name='设备IP地址', blank=True, null=True)
    FAccessuser = models.CharField(max_length=32, verbose_name='接入用户名', blank=True, null=True)
    FAccesspwd = models.CharField(max_length=32, verbose_name='接入密码', blank=True, null=True)
    FDevtype = models.IntegerField(choices=TYPE_CHOICES, verbose_name='设备类型', blank=True, null=True)
    FIsYuntai = models.BooleanField(default=False, verbose_name='是否云台控制')
    FChannelNo = models.CharField(max_length=32, verbose_name='通道号', blank=True, null=True)
    FPort = models.IntegerField(verbose_name='端口号', blank=True, null=True)
    FProtocoltype = models.IntegerField(choices=PROTOCOL_CHOICES, verbose_name='接入协议', blank=True, null=True)
    FProtocol = models.CharField(max_length=128, verbose_name='协议地址', blank=True, null=True)
    FAreaID = models.CharField(max_length=32, verbose_name='安装区域', blank=True, null=True)
    FTransmode = models.IntegerField(choices=TRANSMODE_CHOICES, verbose_name='传输方式', blank=True, null=True)
    FIsOpenAudio = models.BooleanField(default=True, verbose_name='开启音频')
    FIsOpenVideo = models.BooleanField(default=True, verbose_name='开启视频')
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        db_table = 'T_MonitorDev'

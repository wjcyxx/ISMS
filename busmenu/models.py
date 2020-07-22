from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class busmenu(models.Model):
    MENUPOS_CHOICES = (
        (None, '请选择数据'),
        (0, '顶部'),
        (1, '侧边'),
        (2, '数据中心')
    )

    FLOD_CHOICES = (
        (None, '请选择数据'),
        (0, '折叠'),
        (1, '展开')
    )

    NEWFORM_CHOICES = (
        (None, '请选择数据'),
        (0, '嵌入式'),
        (1, '新窗口'),
        (2, '原窗口全屏')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FSequence = models.IntegerField(verbose_name='顺序号', blank=True, null=True)
    FGroupID = models.IntegerField(verbose_name='菜单组', blank=True, null=True)
    FMenuID = models.CharField(max_length=32, verbose_name='菜单ID', blank=True, null=True)
    FMenuName = models.CharField(max_length=32, verbose_name='菜单名称', blank=True, null=True)
    FUrl = models.CharField(max_length=100, verbose_name='菜单地址', blank=True, null=True)
    FMenuIcon = models.CharField(max_length=32, verbose_name='菜单图标', blank=True, null=True)
    FMenuPosition = models.IntegerField(choices=MENUPOS_CHOICES, default=0, verbose_name='菜单位置', blank=True, null=True)
    FFoldState = models.IntegerField(choices=FLOD_CHOICES, default=0, verbose_name='菜单折叠', blank=True, null=True)
    FFormState = models.IntegerField(choices=NEWFORM_CHOICES, default=0, verbose_name='打开模式', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Menu'


class authmenu(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FUserGroupID = models.CharField(max_length=32, verbose_name='用户组FID', blank=True, null=True)
    FBusMenuID = models.CharField(max_length=32, verbose_name='菜单ID', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_AuthMenu'
from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class busmenu(models.Model):
    MENUPOS_CHOICES = (
        (0, None),
        (1, '顶部'),
        (2, '侧边')

    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FSequence = models.IntegerField(verbose_name='顺序号', blank=True, null=True)
    FMenuID = models.CharField(max_length=32, verbose_name='菜单ID', blank=True, null=True)
    FMenuName = models.CharField(max_length=32, verbose_name='菜单名称', blank=True, null=True)
    FUrl = models.CharField(max_length=100, verbose_name='菜单地址', blank=True, null=True)
    FMenuIcon = models.CharField(max_length=32, verbose_name='菜单图标', blank=True, null=True)
    FMenuPosition = models.IntegerField(choices=MENUPOS_CHOICES, default=0, verbose_name='菜单位置', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Menu'

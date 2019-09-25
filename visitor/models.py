from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

@python_2_unicode_compatible

class visitor(models.Model):

    SEX_CHOICES = (
        (None, '请选择数据'),
        (0, '男'),
        (1, '女')
    )

    STATUS_CHOICES = (
        (None, '请选择数据'),
        (0, '登记'),
        (1, '退场'),
        (2, '禁用')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FName = models.CharField(max_length=32, verbose_name='访客姓名', blank=True, null=True)
    FOriginName = models.CharField(max_length=100, verbose_name='所属组织', blank=True, null=True)
    FSex = models.IntegerField(choices=SEX_CHOICES, verbose_name='性别', blank=True, null=True)
    FVisitorIDcard = models.CharField(max_length=18, verbose_name='访客身份证', blank=True, null=True)
    FReceptionist = models.CharField(max_length=32, verbose_name='接待人', blank=True, null=True)
    FValidDate = models.DateField(blank=True, null=True, verbose_name='有效日期')
    FRefundDate = models.DateTimeField(blank=True, null=True, verbose_name='退卡时间')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Visitor'

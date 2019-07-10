from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible
import urllib
from django.core.files import File
import os

# Create your models here.

@python_2_unicode_compatible

class organize(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FOrgID = models.CharField(max_length=32, verbose_name='统一社会信用代码', unique=True, error_messages={'unique': '信用代码重复'})
    FQualevel = models.CharField(max_length=32, verbose_name='主项资质等级', blank=True, null=True)
    FOrgname = models.CharField(max_length=32, verbose_name='组织名称', unique=True, error_messages={'unique': '组织名称重复'})
    FOrgtypeID = models.CharField(max_length=32, verbose_name='组织类型')
    provid = models.CharField(max_length=32, verbose_name='所属省份', blank=True, null=True)
    cityid = models.CharField(max_length=32, verbose_name='所属城市', blank=True, null=True)
    areaid = models.CharField(max_length=32, verbose_name='所属区域', blank=True, null=True)
    FOrgaddress = models.CharField(max_length=128, verbose_name='组织地址', blank=True, null=True)
    FLong = models.FloatField(verbose_name='经度', blank=True, null=True)
    FLat = models.FloatField(verbose_name='经度', blank=True, null=True)
    FLar = models.CharField(max_length=32, verbose_name='法人代表', blank=True, null=True)
    FLartel = models.CharField(max_length=32, verbose_name='法人代表电话', blank=True, null=True)
    FLarIDcard = models.CharField(max_length=50, verbose_name='法人代表身份证', blank=True, null=True)
    FRegcapital = models.DecimalField(max_digits=32, decimal_places=8, verbose_name='注册资金', blank=True, null=True)
    FRegDate = models.DateField(verbose_name='注册日期', blank=True, null=True)
    FLicenceno = models.CharField(max_length=128, verbose_name='安全施工许可证号', blank=True, null=True)
    FValidDate = models.DateField(verbose_name='许可证有效日期', blank=True, null=True)
    FLicauthority = models.CharField(max_length=32, verbose_name='发证机关', blank=True, null=True)
    FHrcharge = models.CharField(max_length=32, verbose_name='劳资负责人姓名', blank=True, null=True)
    FHrIDcard = models.CharField(max_length=128, verbose_name='劳资负责人身份证', blank=True, null=True)
    FHrtel = models.CharField(max_length=32, verbose_name='劳资负责人电话', blank=True, null=True)
    FIssplit = models.BooleanField(default=True, verbose_name='是否数据隔离')
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FScope = models.CharField(max_length=1000, verbose_name='经营范围', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "T_Organize"


class orgQualifications(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FQualification = models.CharField(max_length=32, verbose_name='资质名称', blank=True, null=True)
    FFilename = models.CharField(max_length=32, verbose_name='文件名称', blank=True, null=True)
    FFilepath = models.ImageField(upload_to='orgqualpic/', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "T_OrgQualifications"



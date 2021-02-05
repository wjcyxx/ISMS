from django.db import models
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class prjcheck(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPrjID = models.CharField(max_length=32, verbose_name='项目编号', blank=True, null=True)
    FAddress = models.CharField(max_length=100, verbose_name='事件地址', blank=True, null=True)
    FProblem = models.CharField(max_length=100, verbose_name='问题名称', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='事件描述', blank=True, null=True)
    FPic = models.ImageField(upload_to='itemcheckpic/', default='', verbose_name='检查图片', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_PrjCheck'


class prjcheckpic(models.Model):
    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, verbose_name='项目编号', blank=True, null=True)
    FPic = models.ImageField(upload_to='itemcheckpic/', default='', verbose_name='检查图片', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_PrjCheckPic'
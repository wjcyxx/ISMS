from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class team(models.Model):
    EVAL_CHOICES = (
        (0, '合格'),
        (1, '不合格')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FOrgID = models.CharField(max_length=32, verbose_name='所属分包商', blank=True, null=True)
    FName = models.CharField(max_length=32, verbose_name='施工队名称', blank=True, null=True)
    FTeammgr = models.CharField(max_length=32, verbose_name='项目经理', blank=True, null=True)
    FMgrtel = models.CharField(max_length=32, verbose_name='联系电话', blank=True, null=True)
    FIDcard = models.CharField(max_length=32, verbose_name='身份证', blank=True, null=True)
    FFirstDate = models.DateField(verbose_name='合同签订日期', blank=True, null=True)
    FScope = models.CharField(max_length=128, verbose_name='承包范围', blank=True, null=True)
    FAmount = models.FloatField(verbose_name='承包金额', blank=True, null=True)
    FEvaluate = models.IntegerField(choices=EVAL_CHOICES, default=0, verbose_name='评价')
    FScale = models.IntegerField(verbose_name='队伍规模', blank=True, null=True)
    FSource = models.CharField(max_length=32, verbose_name='队伍来源', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "T_Team"



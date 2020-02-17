from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class prjprocess(models.Model):
    PLAN_STATUS_CHOICES = (
        (None, '请选择数据'),
        (0, '计划中'),
        (1, '已完成')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FProcessName = models.CharField(max_length=50, verbose_name='阶段名称', blank=True, null=True)
    FScheduleTime = models.DateField(verbose_name='计划日期', blank=True, null=True)
    FPlanStatus = models.IntegerField(default=0, choices=PLAN_STATUS_CHOICES, verbose_name='阶段状态', blank=True, null=True)
    FCompleteTime = models.DateField(verbose_name='完成日期', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "T_PrjProcess"

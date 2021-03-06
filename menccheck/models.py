from django.db import models
import uuid
from menchanical.models import menchanical
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class menccheck(models.Model):


    RESULT_CHOICES = (
        (None, '请选择数据'),
        (0, '正常'),
        (1, '异常')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FMecserialFID = models.ForeignKey(menchanical, to_field='FID', on_delete=models.PROTECT, blank=True, null=True)
    FCheckPersonID = models.CharField(max_length=32, verbose_name='检查人员ID', blank=True, null=True)
    FCheckdate = models.DateField(verbose_name='检查日期', blank=True, null=True)
    FCheckitemID = models.CharField(max_length=32, verbose_name='检查项目', blank=True, null=True)
    FCheckresult = models.IntegerField(choices=RESULT_CHOICES, verbose_name='检查结果', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_MecCheckLog'

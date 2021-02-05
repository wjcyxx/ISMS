from django.db import models
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class abnpound(models.Model):

    RESULT_CHOICES = (
        (None, '请选择数据'),
        (0, '异常收货'),
        (1, '退货'),
        (2, '作废')
    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPoundID = models.CharField(max_length=32, verbose_name='磅单ID', blank=True, null=True)
    FResult = models.IntegerField(choices=RESULT_CHOICES, verbose_name='处理结果', blank=True, null=True)
    FResultDate = models.DateField(verbose_name='处理时间', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='描述', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_AbnormalPound'


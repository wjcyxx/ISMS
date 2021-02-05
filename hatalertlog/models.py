from django.db import models
from personnel.models import personnel
from hatrule.models import hatrule
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class hatalertlog(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    #FRuleID = models.CharField(max_length=32, verbose_name='规则id', blank=True, null=True)
    FRuleID = models.ForeignKey(hatrule, to_field='FID', on_delete=models.CASCADE, blank=True, null=True, verbose_name='规则ID')
    FPersonID = models.ForeignKey(personnel, to_field='FID', on_delete=models.CASCADE, blank=True, null=True, verbose_name='人员ID')
    FPicPath = models.ImageField(upload_to='hatalert/', verbose_name='报警图片', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_HatAlertLog'


from django.db import models
from personnel.models import personnel
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class safetrain(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FTraintypeID = models.CharField(max_length=32, verbose_name='培训类型', blank=True, null=True)
    FSubject = models.CharField(max_length=128, verbose_name='培训主题', blank=True, null=True)
    FTrainDate = models.DateField(verbose_name='培训日期', blank=True, null=True)
    FTrainTeacher = models.CharField(max_length=32, verbose_name='培训人', blank=True, null=True)
    FTrainHour = models.IntegerField(verbose_name='培训课时', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        db_table = 'T_SafeTrain'


class safetrainperson(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FPersonID = models.ForeignKey(personnel, to_field='FID', on_delete=models.CASCADE, blank=True, null=True, verbose_name='人员ID')
    FIsQualified = models.BooleanField(verbose_name='是否合格', default=True)
    FScore = models.IntegerField(verbose_name='培训得分', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_SafeTrainPerson'
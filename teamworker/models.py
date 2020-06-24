from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class teamworker(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FTeamWorkerTypeID = models.CharField(max_length=32, verbose_name='协作类型', blank=True, null=True)
    FTitle = models.CharField(max_length=200, verbose_name='标题', blank=True, null=True)
    FDeadLine = models.DateField(verbose_name='完成期限', blank=True, null=True)
    FLevel = models.CharField(max_length=32, verbose_name='优先级', blank=True, null=True)
    FTag = models.CharField(max_length=100, verbose_name='标识', blank=True, null=True)
    FBimModel = models.CharField(max_length=200, verbose_name='关联BIM', blank=True, null=True)
    FPic = models.ImageField(upload_to='twpic/', default='', verbose_name='协同图片', blank=True, null=True)
    FRecord = models.ImageField(upload_to='twrecord/', default='', verbose_name='录音', blank=True, null=True)
    FStakeholder = models.CharField(max_length=1000, verbose_name='干系人', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        db_table = 'T_TeamWorkerInfo'
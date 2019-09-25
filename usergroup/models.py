from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class usergroup(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FName = models.CharField(max_length=32, verbose_name='用户组名称', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_UserGroup'

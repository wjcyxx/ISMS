from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class User(models.Model):

    TYPE_CHOICES = (
        (0, '企业账户'),
        (1, '合作伙伴'),
        (3, '管理员')
    )


    FID = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    FUserID = models.CharField(max_length=32, verbose_name='用户账户')
    FUserpwd = models.CharField(max_length=32, verbose_name='用户密码')
    FType = models.IntegerField(choices=TYPE_CHOICES, verbose_name='用户类型', default=0)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FUsername = models.CharField(max_length=32, verbose_name='用户名称', blank=True, null=True)
    FOrgID = models.CharField(max_length=32, verbose_name='所属组织', blank=True, null=True)
    FRoleID = models.CharField(max_length=32, verbose_name='角色', blank=True, null=True)
    FTel = models.CharField(max_length=32, verbose_name='联系电话', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "T_User"

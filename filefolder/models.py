from django.db import models
import uuid
from six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
#文件夹模型
class filefolder(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FFolderNo = models.CharField(max_length=100, verbose_name='文件夹序号', blank=True, null=True)
    FFolderName = models.CharField(max_length=300, verbose_name='文件夹名称', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_FileFolder'

#上传文件模型
class uploadfiles(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FFolderID = models.CharField(max_length=32, verbose_name='所属文件夹ID', blank=True, null=True)
    FFile = models.ImageField(upload_to='prjfile/', default='', verbose_name='项目文件', blank=True, null=True)
    FFileType = models.CharField(max_length=32, verbose_name='文件类型', blank=True, null=True)
    FFileDesc = models.CharField(max_length=32, verbose_name='文件描述', blank=True, null=True)
    FUploader = models.CharField(max_length=50, verbose_name='上传人员', blank=True, null=True)
    FUnionBimModel = models.CharField(max_length=200, verbose_name='关联模型', blank=True, null=True)
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_UploadFiles'
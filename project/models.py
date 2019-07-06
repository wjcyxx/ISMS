from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class project(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    FPrjID = models.CharField(max_length=32, verbose_name='项目编码')
    FPrjname = models.CharField(max_length=128, verbose_name='项目名称')
    FShortname = models.CharField(max_length=128, verbose_name='项目简称', blank=True, null=True)
    FPrjtypeID = models.CharField(max_length=32, verbose_name='工程类别')
    FPrjuseID = models.CharField(max_length=32, verbose_name='工程用途')

    class Meta:
        db_table = "T_Project"

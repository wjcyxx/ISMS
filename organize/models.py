from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class organize(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    FOrgID = models.CharField(max_length=32, verbose_name='统一社会信用代码', blank=True, null=True)
    FQualevel = models.CharField(max_length=32, verbose_name='主项资质等级', blank=True, null=True)
    FOrgname = models.CharField(max_length=32, verbose_name='组织名称')
    FOrgtypeID = models.CharField(max_length=32, verbose_name='组织类型')

    class Meta:
        db_table = "T_Organize"


from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class teamworker(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FTeamWorkerTypeID = models.CharField(max_length=32, verbose_name='协作类型', blank=True, null=True)
    FTitle = models.CharField(max_length=200, verbose_name='标题', blank=True, null=True)


    class Meta:
        db_table = 'T_TeamWorkerInfo'
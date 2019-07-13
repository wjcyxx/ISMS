from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class team(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FOrgID = models.CharField(max_length=32, verbose_name='所属分包商', blank=True, null=True)

    class Meta:
        db_table = "T_Team"
from django.db import models

# Create your models here.

class sequence(models.Model):

    id = models.AutoField(primary_key=True)
    FPrefix = models.CharField(max_length=32, verbose_name='前缀', blank=True, null=True)
    FDate = models.DateField(verbose_name='日期', blank=True, null=True)
    FSequence = models.IntegerField(verbose_name='顺序号', blank=True, null=True)

    class Meta:
        db_table = 'T_Sequence'
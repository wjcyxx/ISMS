# Generated by Django 2.1.4 on 2019-08-12 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abnpound', '0002_abnpound_fresultdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abnpound',
            name='FResult',
            field=models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '异常收货'), (1, '退货'), (2, '作废')], null=True, verbose_name='处理结果'),
        ),
    ]

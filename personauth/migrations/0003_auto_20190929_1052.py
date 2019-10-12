# Generated by Django 2.1.4 on 2019-09-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personauth', '0002_personauthmode'),
    ]

    operations = [
        migrations.AddField(
            model_name='personauthmode',
            name='FAuthtimequm',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='授权时间段'),
        ),
        migrations.AddField(
            model_name='personauthmode',
            name='FAuthvalidity',
            field=models.DateTimeField(blank=True, null=True, verbose_name='授权有效期'),
        ),
        migrations.AddField(
            model_name='personauthmode',
            name='FStatus',
            field=models.IntegerField(choices=[(None, '请选择数据'), (0, '生效'), (1, '失效'), (2, '退卡')], default=0, verbose_name='状态'),
        ),
    ]
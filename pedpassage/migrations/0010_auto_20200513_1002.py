# Generated by Django 2.1.4 on 2020-05-13 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedpassage', '0009_auto_20200331_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='passagerecord',
            name='FDeviceID',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='设备ID'),
        ),
        migrations.AddField(
            model_name='passagerecord',
            name='FPictureUrl',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='现场照URL'),
        ),
        migrations.AddField(
            model_name='passagerecord',
            name='FType',
            field=models.IntegerField(blank=True, null=True, verbose_name='识别结果分类'),
        ),
    ]

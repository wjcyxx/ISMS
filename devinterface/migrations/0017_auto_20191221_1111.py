# Generated by Django 2.1.4 on 2019-12-21 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterface', '0016_devinterface_fappfid'),
    ]

    operations = [
        migrations.AddField(
            model_name='devinterface',
            name='FCallSigCode',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='调用特征码'),
        ),
        migrations.AddField(
            model_name='devinterface',
            name='FScope',
            field=models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '项目'), (1, '组织'), (2, '全局')], default=0, null=True, verbose_name='适配范围'),
        ),
    ]

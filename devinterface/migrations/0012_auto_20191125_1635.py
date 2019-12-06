# Generated by Django 2.1.4 on 2019-11-25 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterface', '0011_auto_20191030_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='devinterface',
            name='FSrvFile',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='服务文件'),
        ),
        migrations.AddField(
            model_name='devinterface',
            name='FSrvStatus',
            field=models.BooleanField(default=False, verbose_name='服务状态'),
        ),
    ]
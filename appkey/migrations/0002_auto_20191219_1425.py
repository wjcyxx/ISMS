# Generated by Django 2.2 on 2019-12-19 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appkey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appkey',
            name='FAppID',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='appkey'),
        ),
        migrations.AddField(
            model_name='appkey',
            name='FAppSecret',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='appkey'),
        ),
        migrations.AddField(
            model_name='appkey',
            name='FType',
            field=models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '内部应用'), (1, '外部应用')], default=0, null=True, verbose_name='APP类型'),
        ),
        migrations.AlterField(
            model_name='appkey',
            name='FAppkey',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='appkey'),
        ),
    ]
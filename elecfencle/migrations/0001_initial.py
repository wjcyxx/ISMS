# Generated by Django 2.1.4 on 2019-08-01 20:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='elecfencle',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FElecFence', models.CharField(blank=True, max_length=32, null=True, verbose_name='围栏名称')),
                ('FMonitortype', models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '所有车辆'), (1, '选定车辆')], null=True, verbose_name='监控方式')),
                ('FPlate', models.CharField(blank=True, max_length=32, null=True, verbose_name='监控车牌')),
                ('FElecFenceCoordinate', models.CharField(blank=True, max_length=1024, null=True, verbose_name='围栏坐标')),
                ('FDeviation', models.FloatField(blank=True, null=True, verbose_name='报警偏离距离')),
                ('FCoordinatetype', models.IntegerField(choices=[(0, '百度经纬度'), (1, 'GPS经纬度'), (2, '国测局经纬度')], default=0, verbose_name='坐标类型')),
                ('FStatus', models.BooleanField(default=True, verbose_name='状态')),
                ('FDesc', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_ElecFencle',
            },
        ),
    ]

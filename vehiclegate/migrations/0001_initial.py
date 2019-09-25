# Generated by Django 2.1.4 on 2019-07-31 17:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='vehiclegate',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FGate', models.CharField(blank=True, max_length=32, null=True, verbose_name='通道名称')),
                ('FDevID', models.CharField(blank=True, max_length=32, null=True, verbose_name='设备ID')),
                ('FAreaID', models.CharField(blank=True, max_length=32, null=True, verbose_name='区域ID')),
                ('FGatetype', models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '入口'), (1, '出口')], null=True, verbose_name='通道类型')),
                ('FGateattr', models.IntegerField(choices=[(0, '普通通道'), (1, '货运称重通道')], default=0, verbose_name='通道属性')),
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
                'db_table': 'T_VehicleGate',
            },
        ),
    ]

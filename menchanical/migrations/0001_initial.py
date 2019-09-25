# Generated by Django 2.1.4 on 2019-08-12 21:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='menchanical',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FMecserialID', models.CharField(blank=True, max_length=32, null=True, verbose_name='机械唯一编码')),
                ('FMectypeID', models.CharField(blank=True, max_length=32, null=True, verbose_name='机械类型')),
                ('FMecspec', models.CharField(blank=True, max_length=32, null=True, verbose_name='机械型号')),
                ('FMecsource', models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '自有'), (1, '租赁')], null=True, verbose_name='机械来源')),
                ('FOwnerOrg', models.CharField(blank=True, max_length=100, null=True, verbose_name='产权单位')),
                ('FRecordNo', models.CharField(blank=True, max_length=100, null=True, verbose_name='产权备案号')),
                ('FRecorddate', models.DateField(blank=True, null=True, verbose_name='备案日期')),
                ('FLease', models.CharField(blank=True, max_length=32, null=True, verbose_name='机械租赁单位')),
                ('FManufacturer', models.CharField(blank=True, max_length=32, null=True, verbose_name='生产厂商')),
                ('FProducdate', models.DateField(blank=True, null=True, verbose_name='出厂日期')),
                ('FProducNo', models.CharField(blank=True, max_length=32, null=True, verbose_name='出厂编号')),
                ('FMonitordevID', models.CharField(blank=True, max_length=32, null=True, verbose_name='监控设备ID')),
                ('FMecmanager', models.CharField(blank=True, max_length=32, null=True, verbose_name='机械管理员')),
                ('FMecmanagertel', models.CharField(blank=True, max_length=32, null=True, verbose_name='联系方式')),
                ('FParameter', models.CharField(blank=True, max_length=32, null=True, verbose_name='机械参数')),
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
                'db_table': 'T_Menchanical',
            },
        ),
    ]

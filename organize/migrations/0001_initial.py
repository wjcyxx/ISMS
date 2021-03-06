# Generated by Django 2.1.4 on 2019-07-04 00:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='organize',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('FOrgID', models.CharField(blank=True, max_length=32, null=True, verbose_name='统一社会信用代码')),
                ('FQualevel', models.CharField(blank=True, max_length=32, null=True, verbose_name='主项资质等级')),
                ('FOrgname', models.CharField(max_length=32, verbose_name='组织名称')),
                ('FOrgtypeID', models.CharField(max_length=32, verbose_name='组织类型')),
                ('provid', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属省份')),
                ('cityid', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属城市')),
                ('areaid', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属区域')),
                ('FOrgaddress', models.CharField(blank=True, max_length=128, null=True, verbose_name='组织地址')),
                ('FLong', models.FloatField(blank=True, null=True, verbose_name='经度')),
                ('FLat', models.FloatField(blank=True, null=True, verbose_name='经度')),
                ('FLar', models.CharField(blank=True, max_length=32, null=True, verbose_name='法人代表')),
                ('FLartel', models.CharField(blank=True, max_length=32, null=True, verbose_name='法人代表电话')),
                ('FLarIDcard', models.CharField(blank=True, max_length=50, null=True, verbose_name='法人代表身份证')),
                ('FRegcapital', models.DecimalField(blank=True, decimal_places=8, max_digits=32, null=True, verbose_name='注册资金')),
                ('FRegDate', models.DateField(blank=True, null=True, verbose_name='注册日期')),
                ('FLicenceno', models.CharField(blank=True, max_length=128, null=True, verbose_name='安全施工许可证号')),
                ('FValidDate', models.DateField(blank=True, null=True, verbose_name='许可证有效日期')),
                ('FLicauthority', models.CharField(blank=True, max_length=32, null=True, verbose_name='发证机关')),
                ('FHrcharge', models.CharField(blank=True, max_length=32, null=True, verbose_name='劳资负责人姓名')),
                ('FHrIDcard', models.CharField(blank=True, max_length=128, null=True, verbose_name='劳资负责人身份证')),
                ('FHrtel', models.CharField(blank=True, max_length=32, null=True, verbose_name='劳资负责人电话')),
                ('FIssplit', models.BooleanField(default=True, verbose_name='是否数据隔离')),
                ('FStatus', models.BooleanField(default=True, verbose_name='状态')),
                ('FScope', models.CharField(blank=True, max_length=1000, null=True, verbose_name='经验范围')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_Organize',
            },
        ),
    ]

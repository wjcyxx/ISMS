# Generated by Django 2.1.4 on 2019-08-03 09:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='goodstype',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPID', models.CharField(blank=True, max_length=32, null=True)),
                ('FGoodsTypeID', models.CharField(blank=True, max_length=32, null=True, verbose_name='物料类型编号')),
                ('FGoodsType', models.CharField(blank=True, max_length=32, null=True, verbose_name='物料类型')),
                ('FDeviationType', models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '比例偏差'), (1, '范围偏差')], null=True, verbose_name='偏差类别')),
                ('FPositiveDeviation', models.FloatField(blank=True, null=True, verbose_name='正偏差')),
                ('FNegativeDeviation', models.FloatField(blank=True, null=True, verbose_name='负偏差')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_GoodsType',
            },
        ),
    ]

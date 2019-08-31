# Generated by Django 2.1.4 on 2019-08-06 14:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('receaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='materaccountgoods',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPID', models.CharField(blank=True, max_length=32, null=True, verbose_name='FPID')),
                ('FMaterID', models.CharField(blank=True, max_length=32, null=True, verbose_name='物料编码')),
                ('FWaybillQty', models.FloatField(blank=True, null=True, verbose_name='运单数量')),
                ('FUnitID', models.CharField(blank=True, max_length=32, null=True, verbose_name='计量单位')),
                ('FConfirmQty', models.FloatField(blank=True, null=True, verbose_name='确认数量')),
                ('FDeviationQty', models.FloatField(blank=True, null=True, verbose_name='偏差')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_MaterialsAccountGoods',
            },
        ),
    ]
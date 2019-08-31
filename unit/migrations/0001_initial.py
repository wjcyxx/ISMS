# Generated by Django 2.1.4 on 2019-08-04 13:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='unit',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FUnit', models.CharField(blank=True, max_length=32, null=True, verbose_name='计量单位名称')),
                ('FUnitgroupID', models.CharField(blank=True, max_length=32, null=True, verbose_name='计量单位组')),
                ('FIsBaseunit', models.BooleanField(blank=True, default=False, null=True, verbose_name='是否基准单位')),
                ('FConversion', models.FloatField(blank=True, null=True, verbose_name='换算关系')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_Unit',
            },
        ),
    ]
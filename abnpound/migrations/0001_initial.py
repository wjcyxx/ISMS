# Generated by Django 2.1.4 on 2019-08-12 14:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='abnpound',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPoundID', models.CharField(blank=True, max_length=32, null=True, verbose_name='磅单ID')),
                ('FResult', models.IntegerField(blank=True, choices=[(0, '异常收货'), (1, '退货'), (2, '作废')], null=True, verbose_name='处理结果')),
                ('FDesc', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_AbnormalPound',
            },
        ),
    ]

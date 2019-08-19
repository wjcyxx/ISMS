# Generated by Django 2.1.4 on 2019-08-18 09:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menchanical', '0004_mecoperlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='mencrepairlog',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FSubmitter', models.CharField(blank=True, max_length=32, null=True, verbose_name='故障提交人')),
                ('FSubmitdate', models.DateField(blank=True, null=True, verbose_name='提交日期')),
                ('FHappendate', models.DateField(blank=True, null=True, verbose_name='故障发生时间')),
                ('FSite', models.CharField(blank=True, max_length=32, null=True, verbose_name='发生部位')),
                ('FDesc', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('FMecserialFID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menchanical.menchanical')),
            ],
            options={
                'db_table': 'T_MencRepairLog',
            },
        ),
    ]

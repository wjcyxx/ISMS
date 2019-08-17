# Generated by Django 2.1.4 on 2019-08-17 09:23

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
            name='mencrepairplan',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FChecktype', models.IntegerField(blank=True, choices=[(None, '请选择数据'), (0, '固定频率'), (1, '随机抽查')], null=True, verbose_name='检查类型')),
                ('FInterval', models.IntegerField(blank=True, null=True, verbose_name='固定频率时间')),
                ('FFirstcheckdate', models.DateField(blank=True, null=True, verbose_name='首次检查日期')),
                ('FStatus', models.BooleanField(default=True, verbose_name='状态')),
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
                'db_table': 'T_MencRepairPlan',
            },
        ),
    ]

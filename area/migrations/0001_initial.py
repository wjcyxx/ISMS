# Generated by Django 2.1.4 on 2019-07-12 20:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='area',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FName', models.CharField(max_length=128, verbose_name='区域名称')),
                ('FPosition', models.CharField(blank=True, max_length=128, null=True, verbose_name='区域位置')),
                ('FIsCheckworkatten', models.BooleanField(default=True, verbose_name='是否考勤')),
                ('FDesc', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('FStatus', models.BooleanField(default=True, verbose_name='状态')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_ProjectArea',
            },
        ),
    ]

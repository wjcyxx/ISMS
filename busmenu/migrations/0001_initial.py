# Generated by Django 2.1.4 on 2019-09-19 14:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='busmenu',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPID', models.CharField(blank=True, max_length=32, null=True)),
                ('FSequence', models.IntegerField(blank=True, null=True, verbose_name='顺序号')),
                ('FMenuID', models.CharField(blank=True, max_length=32, null=True, verbose_name='菜单ID')),
                ('FMenuName', models.CharField(blank=True, max_length=32, null=True, verbose_name='菜单名称')),
                ('FUrl', models.CharField(blank=True, max_length=100, null=True, verbose_name='菜单地址')),
                ('FMenuIcon', models.CharField(blank=True, max_length=32, null=True, verbose_name='菜单图标')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_Menu',
            },
        ),
    ]

# Generated by Django 2.1.4 on 2019-07-22 22:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('personauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='personauthmode',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPersonID', models.CharField(blank=True, max_length=32, null=True, verbose_name='人员ID')),
                ('FAuthtypeID', models.CharField(blank=True, max_length=32, null=True, verbose_name='授权类型')),
                ('FFeaturevalue', models.CharField(blank=True, max_length=3072, null=True, verbose_name='特征值')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_PersonAuthMode',
            },
        ),
    ]

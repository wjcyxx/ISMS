# Generated by Django 2.1.4 on 2019-07-10 11:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0004_auto_20190710_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='orgQualifications',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPID', models.CharField(blank=True, max_length=32, null=True)),
                ('FQualification', models.CharField(blank=True, max_length=32, null=True, verbose_name='资质名称')),
                ('FFilename', models.CharField(blank=True, max_length=32, null=True, verbose_name='文件名称')),
                ('FFilepath', models.ImageField(upload_to='orgqualpic/')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_OrgQualifications',
            },
        ),
    ]
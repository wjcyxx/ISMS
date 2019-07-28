# Generated by Django 2.1.4 on 2019-07-28 09:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personnel', '0009_auto_20190718_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='hatalertlog',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FRuleID', models.CharField(blank=True, max_length=32, null=True, verbose_name='规则id')),
                ('FPicPath', models.ImageField(blank=True, null=True, upload_to='hatalert/', verbose_name='报警图片')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('FPersonID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personnel.personnel', verbose_name='人员ID')),
            ],
            options={
                'db_table': 'T_HatAlertLog',
            },
        ),
    ]

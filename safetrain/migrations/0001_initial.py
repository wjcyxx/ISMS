# Generated by Django 2.1.4 on 2019-07-28 13:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='safetrain',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FTraintypeID', models.CharField(blank=True, max_length=32, null=True, verbose_name='培训类型')),
                ('FSubject', models.CharField(blank=True, max_length=128, null=True, verbose_name='培训主题')),
                ('FTrainDate', models.DateField(blank=True, null=True, verbose_name='培训日期')),
                ('FTrainTeacher', models.CharField(blank=True, max_length=32, null=True, verbose_name='培训人')),
                ('FTrainHour', models.IntegerField(blank=True, null=True, verbose_name='培训课时')),
                ('FDesc', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'T_SafeTrain',
            },
        ),
    ]
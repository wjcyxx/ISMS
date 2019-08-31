# Generated by Django 2.1.4 on 2019-07-31 15:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('envrule', '0003_auto_20190731_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='envalarmlog',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FDesc', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('FPortID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='envrule.envruleswitch', verbose_name='端口号ID')),
                ('FRuleID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='envrule.envrule', verbose_name='触发规则ID')),
            ],
            options={
                'db_table': 'T_EnvAlarmLog',
            },
        ),
    ]
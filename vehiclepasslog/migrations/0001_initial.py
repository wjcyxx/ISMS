# Generated by Django 2.1.4 on 2019-08-01 15:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehiclegate', '0003_vehiclesigin_fisindefinite'),
        ('vehiclefiles', '0002_auto_20190801_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='vehiclepasslog',
            fields=[
                ('FID', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('FPicturepath', models.ImageField(blank=True, default='', null=True, upload_to='Plate/', verbose_name='抓拍图片')),
                ('CREATED_PRJ', models.CharField(blank=True, max_length=32, null=True, verbose_name='所属项目')),
                ('CREATED_ORG', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建组织')),
                ('CREATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='创建人')),
                ('CREATED_TIME', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('UPDATED_BY', models.CharField(blank=True, max_length=32, null=True, verbose_name='更新人')),
                ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('FGateID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehiclegate.vehiclegate', verbose_name='通道ID')),
                ('FPlate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehiclefiles.vehiclefiles', to_field='FPlate', verbose_name='车牌号码')),
            ],
            options={
                'db_table': 'T_VehiclePassLog',
            },
        ),
    ]

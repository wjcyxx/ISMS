# Generated by Django 2.1.4 on 2019-08-06 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclefiles', '0002_auto_20190801_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclefiles',
            name='FPlate',
            field=models.CharField(default='', max_length=32, unique=True, verbose_name='车牌号码'),
        ),
    ]

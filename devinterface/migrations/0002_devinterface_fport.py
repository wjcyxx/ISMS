# Generated by Django 2.1.4 on 2019-07-21 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devinterface',
            name='FPort',
            field=models.IntegerField(blank=True, null=True, verbose_name='设备端口号'),
        ),
    ]

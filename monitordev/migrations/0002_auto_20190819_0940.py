# Generated by Django 2.1.4 on 2019-08-19 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitordev', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitordev',
            name='FProtocol',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='协议地址'),
        ),
    ]

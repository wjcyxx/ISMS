# Generated by Django 2.1.4 on 2019-11-21 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_devcallinterface'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['FDevtypeID', 'FDevID']},
        ),
        migrations.AddField(
            model_name='devcallinterface',
            name='FDesc',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注'),
        ),
        migrations.AddField(
            model_name='devcallinterface',
            name='FStatus',
            field=models.BooleanField(default=True, verbose_name='状态'),
        ),
    ]

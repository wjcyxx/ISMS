# Generated by Django 2.2 on 2019-10-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterface', '0007_devinterface_finterfaceextid'),
    ]

    operations = [
        migrations.AddField(
            model_name='interfaceparam',
            name='FSequence',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='顺序号'),
        ),
    ]

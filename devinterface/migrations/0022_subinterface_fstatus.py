# Generated by Django 2.1.4 on 2020-03-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterface', '0021_subinterface'),
    ]

    operations = [
        migrations.AddField(
            model_name='subinterface',
            name='FStatus',
            field=models.BooleanField(default=True, verbose_name='状态'),
        ),
    ]

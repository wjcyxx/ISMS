# Generated by Django 2.2 on 2019-07-10 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0002_auto_20190709_2213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='base',
            options={'ordering': ['FBaseID']},
        ),
    ]

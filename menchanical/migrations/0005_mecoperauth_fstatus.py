# Generated by Django 2.1.4 on 2019-11-06 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menchanical', '0004_mecoperlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='mecoperauth',
            name='FStatus',
            field=models.BooleanField(default=True, verbose_name='状态'),
        ),
    ]

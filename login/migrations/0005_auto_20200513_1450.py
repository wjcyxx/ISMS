# Generated by Django 2.1.4 on 2020-05-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200316_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='FUserID',
            field=models.CharField(max_length=32, unique=True, verbose_name='用户账户'),
        ),
    ]

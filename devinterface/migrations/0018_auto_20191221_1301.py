# Generated by Django 2.1.4 on 2019-12-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterface', '0017_auto_20191221_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devinterface',
            name='FCallSigCode',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='调用特征码'),
        ),
    ]
# Generated by Django 2.1.4 on 2019-09-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0004_visitor_freceptionist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='FRefundDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='退卡时间'),
        ),
    ]

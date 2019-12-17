# Generated by Django 2.2 on 2019-12-17 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190712_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='areaid',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='所属区域'),
        ),
        migrations.AddField(
            model_name='project',
            name='cityid',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='所属城市'),
        ),
        migrations.AddField(
            model_name='project',
            name='provid',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='所属省份'),
        ),
    ]

# Generated by Django 2.2 on 2019-07-12 13:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20190712_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='FBeginDate',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='实际工期'),
        ),
        migrations.AlterField(
            model_name='project',
            name='FID',
            field=models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='FSigbeginDate',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='合同工期'),
        ),
    ]

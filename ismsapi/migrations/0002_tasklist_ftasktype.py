# Generated by Django 2.2 on 2020-07-06 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ismsapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='FTaskType',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='任务类型'),
        ),
    ]
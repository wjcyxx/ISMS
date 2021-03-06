# Generated by Django 2.1.4 on 2020-03-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_project_fisfullrenov'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='FDutyPerson',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='留守人员'),
        ),
        migrations.AddField(
            model_name='project',
            name='FIsRepeatWork',
            field=models.BooleanField(default=False, verbose_name='是否报备'),
        ),
        migrations.AddField(
            model_name='project',
            name='FIsReport',
            field=models.BooleanField(default=False, verbose_name='是否报备'),
        ),
        migrations.AddField(
            model_name='project',
            name='FRepeatWorkTime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='复工时间'),
        ),
        migrations.AddField(
            model_name='project',
            name='FReportTime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='报备时间'),
        ),
    ]

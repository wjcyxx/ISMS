# Generated by Django 2.1.4 on 2019-08-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menchanical', '0002_mecoperauth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mecoperauth',
            name='FMecserialID',
        ),
        migrations.AddField(
            model_name='mecoperauth',
            name='FPID',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]

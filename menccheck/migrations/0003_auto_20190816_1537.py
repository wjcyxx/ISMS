# Generated by Django 2.1.4 on 2019-08-16 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menccheck', '0002_auto_20190816_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menccheck',
            name='FMecserialFID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='menchanical.menchanical'),
        ),
    ]

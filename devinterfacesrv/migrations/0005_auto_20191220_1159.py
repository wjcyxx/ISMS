# Generated by Django 2.2 on 2019-12-20 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devinterfacesrv', '0004_interfacesrvdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interfacesrvdata',
            name='FValue',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='值'),
        ),
    ]

# Generated by Django 2.1.4 on 2019-08-03 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodstype', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodstype',
            name='FDesc',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述'),
        ),
    ]
# Generated by Django 2.1.4 on 2019-07-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0008_auto_20190718_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='FSafetrainHour',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='培训课时'),
        ),
    ]

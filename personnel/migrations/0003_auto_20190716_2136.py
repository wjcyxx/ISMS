# Generated by Django 2.1.4 on 2019-07-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0002_auto_20190716_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='FPhoto',
            field=models.ImageField(blank=True, default='', null=True, upload_to='hrpic/', verbose_name='照片'),
        ),
    ]
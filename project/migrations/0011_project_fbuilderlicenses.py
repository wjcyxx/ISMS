# Generated by Django 2.1.4 on 2020-03-31 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20200331_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='FbuilderLicenses',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='施工许可证号'),
        ),
    ]

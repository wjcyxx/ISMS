# Generated by Django 2.1.4 on 2020-03-15 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_project_faffdept'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='FIsFullRenov',
            field=models.BooleanField(default=False, verbose_name='是否全装修交付'),
        ),
    ]

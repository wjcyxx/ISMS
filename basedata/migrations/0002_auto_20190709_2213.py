# Generated by Django 2.1.4 on 2019-07-09 14:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='FID',
            field=models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False),
        ),
    ]

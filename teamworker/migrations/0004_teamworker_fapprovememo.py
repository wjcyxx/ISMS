# Generated by Django 2.2 on 2020-07-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamworker', '0003_teamworkreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamworker',
            name='FApproveMemo',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='审核意见'),
        ),
    ]

# Generated by Django 2.1.4 on 2020-03-04 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20191217_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='FConstrAtten',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='施工单位联系人'),
        ),
        migrations.AddField(
            model_name='project',
            name='FConstrAttenTel',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='施工单位联系人电话'),
        ),
        migrations.AddField(
            model_name='project',
            name='FConstrOrgID',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='施工单位'),
        ),
    ]

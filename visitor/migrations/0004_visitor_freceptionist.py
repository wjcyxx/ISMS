# Generated by Django 2.1.4 on 2019-09-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0003_visitor_foriginname'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='FReceptionist',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='接待人'),
        ),
    ]

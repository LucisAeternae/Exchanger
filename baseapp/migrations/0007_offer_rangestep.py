# Generated by Django 2.1.4 on 2019-01-04 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0006_auto_20190104_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='rangestep',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]

# Generated by Django 2.2.2 on 2019-08-14 22:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190814_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='glassesprescription',
            name='pd_left',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(45)], verbose_name='PD left'),
        ),
        migrations.AddField(
            model_name='glassesprescription',
            name='pd_right',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(45)], verbose_name='PD right'),
        ),
        migrations.AlterField(
            model_name='glassesprescription',
            name='pd',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(90)], verbose_name='PD'),
        ),
    ]

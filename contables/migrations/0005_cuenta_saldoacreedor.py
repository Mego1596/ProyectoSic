# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-14 17:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contables', '0004_auto_20171114_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='saldoAcreedor',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50, validators=[django.core.validators.MinValueValidator(0)], verbose_name='saldo_acreedor'),
        ),
    ]

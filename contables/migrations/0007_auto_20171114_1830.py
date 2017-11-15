# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-15 00:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contables', '0006_auto_20171114_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='estadoComprobacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('debe', models.DecimalField(decimal_places=2, max_digits=50, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='debe')),
                ('haber', models.DecimalField(decimal_places=2, max_digits=50, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='haber')),
            ],
        ),
        migrations.AlterField(
            model_name='detalletransaccion',
            name='debe',
            field=models.DecimalField(decimal_places=2, max_digits=50, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='debe'),
        ),
        migrations.AlterField(
            model_name='detalletransaccion',
            name='haber',
            field=models.DecimalField(decimal_places=2, max_digits=50, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='haber'),
        ),
    ]

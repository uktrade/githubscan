# -*- coding: utf-8 -*-
# Generated by Django 4.2.8 on 2024-01-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jsonstore",
            name="processed_data",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="jsonstore",
            name="scanned_data",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="jsonstore",
            name="uk_bank_holidays",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="jsonstore",
            name="uk_bank_holidays_last_update",
            field=models.DateField(blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 4.0.5 on 2022-08-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("report", "0004_remove_organizationnotificationtarget_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EnterpriseUsers",
            fields=[
                (
                    "email",
                    models.EmailField(
                        max_length=254, primary_key=True, serialize=False
                    ),
                ),
                ("login", models.CharField(blank=True, max_length=100)),
                ("name", models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]

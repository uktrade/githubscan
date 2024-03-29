# -*- coding: utf-8 -*-
# Generated by Django 4.1.7 on 2023-05-31 18:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("report", "0009_teamnotificationtarget_login"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="samlnotificationtarget",
            name="red_alerts_only",
        ),
        migrations.RemoveField(
            model_name="teamnotificationtarget",
            name="red_alerts_only",
        ),
        migrations.AddField(
            model_name="samlnotificationtarget",
            name="no_green_alerts",
            field=models.BooleanField(
                default=True,
                help_text="Set False (checked/on) to receive green status notifications",
            ),
        ),
        migrations.AddField(
            model_name="teamnotificationtarget",
            name="no_green_alerts",
            field=models.BooleanField(
                default=False,
                help_text="Set False (checked/on) to receive green status notifications",
            ),
        ),
    ]

# Generated by Django 2.1.7 on 2019-05-17 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubvulnerabilityalters',
            name='id',
        ),
        migrations.AlterField(
            model_name='githubvulnerabilityalters',
            name='repository',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
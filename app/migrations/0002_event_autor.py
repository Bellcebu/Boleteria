# Generated by Django 5.2 on 2025-06-30 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='autor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

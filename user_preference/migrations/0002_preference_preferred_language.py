# Generated by Django 5.1.2 on 2024-11-18 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_preference', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='preferred_language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

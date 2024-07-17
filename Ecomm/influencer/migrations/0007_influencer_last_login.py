# Generated by Django 4.1.13 on 2024-07-13 10:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0006_remove_influencer_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
# Generated by Django 4.1.13 on 2024-07-14 06:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0008_alter_influencer_options_influencer_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

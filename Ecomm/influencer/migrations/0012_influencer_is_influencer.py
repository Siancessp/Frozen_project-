# Generated by Django 4.1.13 on 2024-07-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0011_remove_influencer_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='is_influencer',
            field=models.BooleanField(default=True),
        ),
    ]
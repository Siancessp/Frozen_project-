# Generated by Django 4.2.5 on 2024-05-25 13:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0003_influencer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='passbook',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]

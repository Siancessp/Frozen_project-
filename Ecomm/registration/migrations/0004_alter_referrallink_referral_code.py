# Generated by Django 5.0.4 on 2024-07-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_referrallink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referrallink',
            name='referral_code',
            field=models.CharField(max_length=20),
        ),
    ]

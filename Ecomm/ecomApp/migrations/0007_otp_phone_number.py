# Generated by Django 4.1.13 on 2024-04-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomApp', '0006_rename_otp_customuser_otp_value_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
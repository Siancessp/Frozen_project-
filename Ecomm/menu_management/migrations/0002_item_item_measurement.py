# Generated by Django 4.1.13 on 2024-03-20 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_measurement',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
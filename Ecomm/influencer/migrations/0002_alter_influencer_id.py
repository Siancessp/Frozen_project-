# Generated by Django 4.2.5 on 2024-05-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencer',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]

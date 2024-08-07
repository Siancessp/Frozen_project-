# Generated by Django 5.0.4 on 2024-07-06 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_remove_addressadmin_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_code', models.CharField(max_length=20, unique=True)),
                ('ip_address', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

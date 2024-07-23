# Generated by Django 4.1.13 on 2024-07-19 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0016_influenceramount'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfluencerLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('influencer_code', models.CharField(max_length=20)),
                ('ip_address', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

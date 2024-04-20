# Generated by Django 4.1.13 on 2024-04-14 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu_management', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('couponcode', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('payment_id', models.CharField(max_length=255)),
                ('order_id', models.CharField(max_length=255)),
                ('signature', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('newname', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('delivery_time', models.CharField(max_length=50)),
                ('order_item_id', models.CharField(max_length=50)),
                ('dicounted_price', models.CharField(max_length=50)),
                ('walet_value', models.CharField(max_length=50)),
                ('pick_up', models.CharField(max_length=50)),
                ('previous_price', models.CharField(max_length=50)),
                ('delivery_price', models.CharField(max_length=50)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_management.item')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

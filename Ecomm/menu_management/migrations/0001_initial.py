# Generated by Django 4.1.13 on 2024-03-16 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecomApp', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('item_photo', models.ImageField(upload_to='item_photos/')),
                ('item_quantity', models.PositiveIntegerField()),
                ('item_old_price', models.FloatField()),
                ('discount', models.IntegerField()),
                ('item_new_price', models.FloatField()),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deal_of_the_day', models.BooleanField(default=False)),
                ('recommended', models.BooleanField(default=False)),
                ('most_popular', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomApp.catagory')),
            ],
        ),
    ]

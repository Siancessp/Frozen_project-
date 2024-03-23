# Generated by Django 4.1.13 on 2024-03-23 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecomApp', '0002_alter_customuser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('add_photo', models.ImageField(upload_to='add_photos/')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomApp.catagory')),
            ],
        ),
    ]
# Generated by Django 5.0.6 on 2024-07-05 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('product_detail', models.CharField(max_length=100)),
                ('category', models.IntegerField()),
                ('price', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]

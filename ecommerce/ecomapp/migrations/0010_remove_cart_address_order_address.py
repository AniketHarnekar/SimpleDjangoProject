# Generated by Django 5.0.6 on 2024-08-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0009_cart_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]

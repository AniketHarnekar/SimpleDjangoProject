# Generated by Django 5.0.6 on 2024-07-12 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0007_order_amt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amt',
            field=models.IntegerField(),
        ),
    ]

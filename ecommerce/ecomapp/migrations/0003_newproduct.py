# Generated by Django 5.0.6 on 2024-07-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_product_product_image_alter_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='newProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Product Name')),
            ],
        ),
    ]

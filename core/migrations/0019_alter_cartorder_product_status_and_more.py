# Generated by Django 5.0.6 on 2024-11-21 16:53

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_cart_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='Product_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('Shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='image',
            field=models.ImageField(default='product.jpg', upload_to=core.models.user_directory_path),
        ),
    ]

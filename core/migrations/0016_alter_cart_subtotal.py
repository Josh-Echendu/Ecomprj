# Generated by Django 5.0.6 on 2024-11-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_cart_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]

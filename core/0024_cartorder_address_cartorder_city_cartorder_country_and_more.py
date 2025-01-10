# Generated by Django 5.0.6 on 2024-11-29 10:49

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_cartorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='mobile',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='saved',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='shipping_method',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', blank=True, length=4, max_length=10, prefix='sku', unique=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='stripe_payment',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tracking_website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

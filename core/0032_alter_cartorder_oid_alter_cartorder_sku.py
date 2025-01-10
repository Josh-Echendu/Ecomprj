# Generated by Django 5.0.6 on 2024-11-29 11:56

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_cartorder_oid_alter_cartorder_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456789', blank=True, length=4, max_length=10, prefix='SKU'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456789', blank=True, length=4, max_length=10, prefix='SKU'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-11-29 11:40

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remove_cartorder_oid_remove_cartorder_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456789', length=4, max_length=10, prefix='', unique=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456789', length=4, max_length=10, prefix='', unique=True),
        ),
    ]

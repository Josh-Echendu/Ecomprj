# Generated by Django 5.0.6 on 2023-09-07 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_productimages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(blank=True, default='100 Days', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='mfd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='specification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.CharField(blank=True, default='10', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(blank=True, default='organic', max_length=100, null=True),
        ),
    ]

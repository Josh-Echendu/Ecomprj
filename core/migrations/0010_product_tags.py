# Generated by Django 5.0.6 on 2024-11-05 22:07

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_product_life_product_mfd_product_specification_and_more'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]

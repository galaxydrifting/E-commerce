# Generated by Django 5.0.4 on 2024-04-25 14:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_product_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, default="N/A", null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="specifications",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, default="N/A", null=True
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="description",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, default="N/A", null=True
            ),
        ),
    ]
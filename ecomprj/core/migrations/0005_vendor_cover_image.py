# Generated by Django 5.0.4 on 2024-04-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_vendor_date_alter_product_vendor"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="cover_image",
            field=models.ImageField(
                default="vendor.jpg", upload_to="user_directory_path"
            ),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bdenapp", "0003_property_provision"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyimage",
            name="images",
            field=models.ImageField(blank=True, null=True, upload_to="more_pictures/"),
        ),
    ]

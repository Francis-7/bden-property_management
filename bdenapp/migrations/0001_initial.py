# Generated by Django 5.1.6 on 2025-02-28 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=250)),
                ("owner", models.CharField(max_length=150)),
                ("price", models.FloatField()),
                (
                    "typeChoice",
                    models.CharField(
                        choices=[
                            ("Apartment", "Apartment"),
                            ("Container", "Container"),
                            ("Land", "Land"),
                        ],
                        max_length=15,
                    ),
                ),
                ("description", models.CharField(max_length=500)),
                ("isAvailable", models.BooleanField(default=True)),
                ("picture", models.ImageField(upload_to="images/")),
                ("uploaded", models.DateField(auto_now_add=True)),
                ("isPairToPair", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "properties",
                "db_table": "property",
                "ordering": ["location"],
            },
        ),
    ]

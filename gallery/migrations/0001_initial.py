# Generated by Django 5.2.1 on 2025-05-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("path", models.CharField(max_length=255)),
                (
                    "image_file",
                    models.FileField(blank=True, null=True, upload_to="images/"),
                ),
                ("description", models.TextField()),
                ("embedding", models.BinaryField()),
                ("similarity", models.FloatField(blank=True, null=True)),
            ],
            options={
                "db_table": "images",
            },
        ),
    ]

# Generated by Django 5.2.1 on 2025-05-17 12:50

import django.db.models.deletion
import gallery.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0002_image_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="path",
        ),
        migrations.AlterField(
            model_name="image",
            name="image_file",
            field=models.FileField(
                blank=True, null=True, upload_to=gallery.models.user_directory_path
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

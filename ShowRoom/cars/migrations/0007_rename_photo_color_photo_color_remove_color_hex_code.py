# Generated by Django 5.1.3 on 2024-11-23 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0006_remove_color_color_photo_color_photo"),
    ]

    operations = [
        migrations.RenameField(
            model_name="color", old_name="photo", new_name="photo_color",
        ),
        migrations.RemoveField(model_name="color", name="hex_code",),
    ]
# Generated by Django 5.1.3 on 2024-11-23 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0003_remove_color_hex_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="color",
            name="hex_code",
            field=models.CharField(blank=True, max_length=7, null=True, unique=True),
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-21 14:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dermachat", "0006_alter_imagemetadata_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="imagemetadata",
            name="prediction",
            field=models.FloatField(default=0.0),
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-15 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor_interface", "0002_doctorclassification_delete_doctorselection"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorclassification",
            name="user_id",
            field=models.UUIDField(blank=True, default=None, null=True),
        ),
    ]

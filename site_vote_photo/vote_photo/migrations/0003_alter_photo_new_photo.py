# Generated by Django 4.1.7 on 2023-03-28 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vote_photo", "0002_alter_notification_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="new_photo",
            field=models.ImageField(blank=True, upload_to="new_photos/%Y/%m/%d"),
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-28 18:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vote_photo", "0003_alter_photo_new_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="new_photo",
            field=models.ImageField(upload_to="new_photos/%Y/%m/%d"),
        ),
    ]

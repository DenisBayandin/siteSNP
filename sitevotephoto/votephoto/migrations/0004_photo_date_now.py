# Generated by Django 4.1.7 on 2023-02-17 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votephoto', '0003_remove_photo_date_now'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='date_now',
            field=models.DateTimeField(null=True),
        ),
    ]

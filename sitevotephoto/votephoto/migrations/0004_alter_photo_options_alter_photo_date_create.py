# Generated by Django 4.1.4 on 2023-01-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votephoto', '0003_alter_photo_count_comment_alter_photo_count_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ('-date_create',), 'verbose_name': 'Фото', 'verbose_name_plural': 'Фотографии'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

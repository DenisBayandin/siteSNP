# Generated by Django 4.1.4 on 2023-01-15 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votephoto', '0008_alter_photo_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='comment',
            table='Comment',
        ),
        migrations.AlterModelTable(
            name='like',
            table='Like',
        ),
        migrations.AlterModelTable(
            name='photo',
            table='Photo',
        ),
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
    ]

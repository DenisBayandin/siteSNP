# Generated by Django 4.0.1 on 2022-12-08 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votephoto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo_145x165',
            field=models.ImageField(blank=True, upload_to='photos_145x165/%Y/%m/%d', verbose_name='Фотография размером 145x165'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_1680x1680',
            field=models.ImageField(blank=True, upload_to='photos_1680x1680/%Y/%m/%d', verbose_name='Фотография размером 1680x1680'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_510x510',
            field=models.ImageField(blank=True, upload_to='photos_510x510/%Y/%m/%d', verbose_name='Фотография размером 510x510'),
        ),
    ]

# Generated by Django 4.1.4 on 2023-01-15 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votephoto', '0009_alter_comment_table_alter_like_table_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='like',
            table='like',
        ),
        migrations.AlterModelTable(
            name='photo',
            table='photo',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]

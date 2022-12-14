# Generated by Django 4.0.6 on 2022-09-13 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_remove_film_genre_film_genres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='genre',
            new_name='genres',
        ),
        migrations.AlterField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(to='backend.genre'),
        ),
    ]

# Generated by Django 4.0.6 on 2022-10-06 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0040_remove_film_favorite_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.film'),
        ),
    ]
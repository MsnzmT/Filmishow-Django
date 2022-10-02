# Generated by Django 4.0.6 on 2022-09-16 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0030_arrivalfilm'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='about',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='dislike',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='like',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='film',
            name='summary',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]
# Generated by Django 4.0.6 on 2022-09-21 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0034_emailverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislike',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='film',
            name='dislike',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='film',
            name='like',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

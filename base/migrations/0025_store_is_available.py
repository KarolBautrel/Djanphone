# Generated by Django 4.0.1 on 2022-01-27 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_store_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-27 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_remove_shipment_courier_remove_shipment_home_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='picture',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]

# Generated by Django 4.0.1 on 2022-02-11 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0071_contact_remove_store_map_remove_ticket_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='body',
            field=models.TextField(max_length=30),
        ),
    ]
# Generated by Django 4.1.4 on 2022-12-13 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery', '0002_transportedby_remove_airport_airport_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='package_number',
            new_name='id',
        ),
    ]

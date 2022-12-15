# Generated by Django 4.1.4 on 2022-12-14 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery', '0006_package_recipient'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.RenameField(
            model_name='transportationevent',
            old_name='deivery_route',
            new_name='delivery_route',
        ),
        migrations.AddField(
            model_name='package',
            name='pay',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plane',
            name='flight_number',
            field=models.CharField(default='SV123', max_length=5, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='truck',
            name='truck_number',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
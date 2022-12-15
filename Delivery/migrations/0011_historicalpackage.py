# Generated by Django 4.1.4 on 2022-12-15 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery', '0010_alter_location_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPackage',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('weight', models.FloatField()),
                ('destination', models.CharField(max_length=100)),
                ('dimensions', models.CharField(default='Small', max_length=100)),
                ('insurance_amount', models.FloatField()),
                ('status', models.CharField(default='In Transit', max_length=100)),
                ('category', models.CharField(default='Regular', max_length=100)),
                ('value', models.FloatField(default=0)),
                ('final_delivery_date', models.DateField()),
                ('recipient', models.CharField(default='John Doe', max_length=100)),
                ('pay', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical package',
                'verbose_name_plural': 'historical packages',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
# Generated by Django 2.1.3 on 2018-11-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_remove_venue_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

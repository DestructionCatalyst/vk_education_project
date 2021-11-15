# Generated by Django 3.2.9 on 2021-11-15 08:28

from django.db import migrations
from insurance_orders import zones


def add_zones(apps, schema_editor):
    Zones = apps.get_model('insurance_orders', 'Zones')
    for zone_name in zones.zones:
        Zones(name=zone_name).save()


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_orders', '0002_auto_20211112_1450'),
    ]

    operations = [
        migrations.RunPython(add_zones),
    ]
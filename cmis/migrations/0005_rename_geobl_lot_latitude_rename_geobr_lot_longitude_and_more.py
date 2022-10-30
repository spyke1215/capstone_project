# Generated by Django 4.0.5 on 2022-10-29 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmis', '0004_rename_latitude_lot_geobl_rename_longitude_lot_geobr_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lot',
            old_name='geobl',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='lot',
            old_name='geobr',
            new_name='longitude',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='geotl',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='geotr',
        ),
    ]

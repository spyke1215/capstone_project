# Generated by Django 4.0.5 on 2022-10-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmis', '0005_rename_geobl_lot_latitude_rename_geobr_lot_longitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lot',
            old_name='latitude',
            new_name='geobl',
        ),
        migrations.RenameField(
            model_name='lot',
            old_name='longitude',
            new_name='geobr',
        ),
        migrations.AddField(
            model_name='lot',
            name='geotl',
            field=models.CharField(default=1231231, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lot',
            name='geotr',
            field=models.CharField(default=1231231, max_length=64),
            preserve_default=False,
        ),
    ]

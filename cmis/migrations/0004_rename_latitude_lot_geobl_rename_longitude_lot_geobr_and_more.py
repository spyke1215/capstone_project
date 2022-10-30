# Generated by Django 4.0.5 on 2022-10-29 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmis', '0003_alter_category_options_alter_cemetery_options_and_more'),
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
            field=models.CharField(default=21323, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lot',
            name='geotr',
            field=models.CharField(default=12312312, max_length=64),
            preserve_default=False,
        ),
    ]

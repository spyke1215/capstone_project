# Generated by Django 4.0.5 on 2022-11-14 20:32
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("cmis", "0004_alter_lot_polygon_alter_section_polygon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cemetery",
            name="zoom",
            field=models.FloatField(),
        ),
    ]

# Generated by Django 4.0.5 on 2022-11-03 14:33
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("cmis", "0003_alter_category_options_alter_cemetery_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lot",
            name="polygon",
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name="section",
            name="polygon",
            field=models.CharField(max_length=1024),
        ),
    ]

# Generated by Django 4.0.5 on 2022-10-31 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmis', '0009_rename_sections_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='polygon',
        ),
        migrations.AddField(
            model_name='section',
            name='polygon',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
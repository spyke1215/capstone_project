# Generated by Django 4.0.5 on 2022-11-02 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('max_layers', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Cemetery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('geolocation', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=64)),
                ('center', models.CharField(max_length=64)),
                ('zoom', models.IntegerField()),
            ],
            options={
                'verbose_name': 'cemetery',
                'verbose_name_plural': 'cemeteries',
            },
        ),
        migrations.CreateModel(
            name='Deceased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('middle_name', models.CharField(max_length=32)),
                ('birth_date', models.DateField()),
                ('death_date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'deceased',
                'verbose_name_plural': 'deceased',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'status',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('polygon', models.CharField(max_length=256)),
                ('cemetery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmis.cemetery')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
            },
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polygon', models.CharField(max_length=128)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmis.category')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmis.section')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmis.status')),
            ],
            options={
                'verbose_name': 'lot',
                'verbose_name_plural': 'lots',
            },
        ),
        migrations.CreateModel(
            name='Grave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deceased', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmis.deceased')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmis.lot')),
            ],
            options={
                'verbose_name': 'grave',
                'verbose_name_plural': 'graves',
            },
        ),
    ]

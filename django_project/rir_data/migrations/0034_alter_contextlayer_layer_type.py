# Generated by Django 3.2.8 on 2022-04-22 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rir_data', '0033_alter_instancecategory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextlayer',
            name='layer_type',
            field=models.CharField(choices=[('ARCGIS', 'ARCGIS'), ('Raster Tile', 'Raster Tile'), ('Geojson', 'Geojson')], default='Raster Tile', max_length=256),
        ),
    ]

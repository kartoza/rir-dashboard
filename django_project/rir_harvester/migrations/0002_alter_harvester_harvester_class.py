# Generated by Django 3.2.8 on 2022-01-04 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rir_harvester', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvester',
            name='harvester_class',
            field=models.CharField(choices=[('rir_harvester.harveters.api_with_geography_and_date.APIWithGeographyAndDate', 'API With Geography And Date'), ('rir_harvester.harveters.using_exposed_api.UsingExposedAPI', 'Harvested using exposed API by external client')], help_text='The type of harvester that will be used.Use class with full package.', max_length=256),
        ),
    ]

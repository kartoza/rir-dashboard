# Generated by Django 3.2.8 on 2022-01-04 08:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rir_data', '0012_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='api_exposed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indicator',
            name='api_note',
            field=models.TextField(blank=True, help_text='Note about the usage of api, can put link that is using API to push the data.', null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='api_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Indicate that API is exposed outside. This API is used for get the data and also post new data.'),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='aggregation_behaviour',
            field=models.CharField(choices=[('Use all available populated geography in current time window', 'Use all available populated geography in current time window'), ('Most recent for each geography', 'Most recent for each geography')], default='Most recent for each geography', max_length=256),
        ),
    ]
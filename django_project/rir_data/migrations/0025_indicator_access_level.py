# Generated by Django 3.2.8 on 2022-03-01 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rir_data', '0024_geometry_dashboard_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='access_level',
            field=models.CharField(choices=[('Public', 'Accessed in public.'), ('Signin', 'Need login to access.')], default='Public', max_length=126),
        ),
    ]

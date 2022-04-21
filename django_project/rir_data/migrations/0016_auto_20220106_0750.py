# Generated by Django 3.2.8 on 2022-01-06 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rir_data', '0015_auto_20220106_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geometryuploader',
            name='file',
        ),
        migrations.CreateModel(
            name='GeometryUploaderFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='upload')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rir_data.geometryuploader')),
            ],
        ),
    ]

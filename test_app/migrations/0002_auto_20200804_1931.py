# Generated by Django 3.0.8 on 2020-08-04 16:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='path',
        ),
        migrations.AddField(
            model_name='images',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='album_logos'),
            preserve_default=False,
        ),
    ]

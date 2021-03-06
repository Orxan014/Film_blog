# Generated by Django 3.1.4 on 2021-01-01 17:10

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0005_auto_20210101_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieshots',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=0, size=[500, 300], upload_to='movie_shots/', verbose_name='Picture'),
        ),
    ]

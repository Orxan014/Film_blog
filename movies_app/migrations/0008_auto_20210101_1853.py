# Generated by Django 3.1.4 on 2021-01-01 18:53

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('movies_app', '0007_auto_20210101_1713'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Comment',
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]
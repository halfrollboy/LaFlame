# Generated by Django 2.2.4 on 2019-08-20 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0002_auto_20190820_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='masters',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]

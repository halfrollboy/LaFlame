# Generated by Django 2.2.4 on 2019-11-06 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0015_auto_20191104_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='day',
            field=models.IntegerField(default=6, verbose_name='День'),
        ),
        migrations.AlterField(
            model_name='date',
            name='month',
            field=models.IntegerField(default=11, verbose_name='Месяц'),
        ),
        migrations.AlterField(
            model_name='date',
            name='year',
            field=models.IntegerField(default=2019, verbose_name='Год'),
        ),
    ]
# Generated by Django 2.2.4 on 2019-08-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0003_masters_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(max_length=30, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='company',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Картинка '),
        ),
        migrations.AlterField(
            model_name='company',
            name='start_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='date',
            name='day',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='date',
            name='month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='date',
            name='procedure',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='date',
            name='time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='date',
            name='year',
            field=models.IntegerField(),
        ),
    ]

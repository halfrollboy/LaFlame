# Generated by Django 2.2.4 on 2020-06-16 05:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0027_newcompany_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationsDetailNas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.IntegerField(verbose_name='Стоимость услуги')),
                ('time', models.TimeField(verbose_name='Время на услугу')),
                ('description', models.TextField(default='no description', verbose_name='Описание услуги')),
                ('main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flesh.Operations')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flesh.Masters')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('date_as', models.DateField(default=datetime.date.today, verbose_name='Дата')),
                ('year', models.IntegerField(default=2020, verbose_name='Год')),
                ('month', models.IntegerField(default=6, verbose_name='Месяц')),
                ('day', models.IntegerField(default=16, verbose_name='День')),
                ('timestart', models.TimeField(verbose_name='Время')),
                ('endtime', models.TimeField(verbose_name='Время')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flesh.Masters')),
            ],
            options={
                'verbose_name': 'Дата',
                'verbose_name_plural': 'Даты',
                'db_table': 'orderdate',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flesh.OrderDate'),
        ),
        migrations.AlterField(
            model_name='order',
            name='operation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flesh.OperationsDetailNas'),
        ),
        migrations.DeleteModel(
            name='Date',
        ),
    ]

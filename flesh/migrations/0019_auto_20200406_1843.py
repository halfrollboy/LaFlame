# Generated by Django 2.2.4 on 2020-04-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0018_auto_20200307_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persent', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Оценка качества')),
                ('klients', models.IntegerField(default=0, verbose_name='Кол-во клиентов')),
            ],
        ),
        migrations.AlterField(
            model_name='date',
            name='day',
            field=models.IntegerField(default=6, verbose_name='День'),
        ),
        migrations.AlterField(
            model_name='date',
            name='month',
            field=models.IntegerField(default=4, verbose_name='Месяц'),
        ),
        migrations.AlterField(
            model_name='masters',
            name='number_m',
            field=models.CharField(blank=True, max_length=12, unique=True, verbose_name='Номер мастера'),
        ),
    ]

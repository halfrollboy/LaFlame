# Generated by Django 2.2.4 on 2020-06-08 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0026_auto_20200608_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='newcompany',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
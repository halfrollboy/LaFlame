# Generated by Django 2.2.4 on 2019-08-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0013_operations'),
    ]

    operations = [
        migrations.AddField(
            model_name='operations',
            name='companys',
            field=models.ManyToManyField(blank=True, related_name='companys', to='flesh.Company'),
        ),
    ]
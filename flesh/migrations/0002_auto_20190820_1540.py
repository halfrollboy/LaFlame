# Generated by Django 2.2.4 on 2019-08-20 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flesh', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='comments',
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviews', models.TextField(blank=True, verbose_name='Отзывы')),
                ('company_r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flesh.Company')),
            ],
        ),
    ]
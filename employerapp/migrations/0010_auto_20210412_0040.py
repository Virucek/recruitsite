# Generated by Django 3.1.1 on 2021-04-12 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0009_auto_20210409_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='currency',
            field=models.CharField(blank=True, choices=[('RUB', 'RUB'), ('USD', 'USD'), ('EUR', 'EUR')], help_text='поле необязательное для заполнения', max_length=4, verbose_name='валюта'),
        ),
    ]

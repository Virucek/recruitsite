# Generated by Django 3.1.1 on 2021-04-12 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20210412_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 9, 56, 26, 992445)),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 9, 56, 26, 999052)),
        ),
    ]

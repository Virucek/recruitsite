# Generated by Django 3.1.1 on 2021-03-21 04:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
        ('jobseekerapp', '0001_initial'),
        ('employerapp', '0003_sendoffers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sendoffers',
            options={'verbose_name_plural': 'Предложения для соискателей'},
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='дата добавления в избранное')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.employer')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobseekerapp.resume', verbose_name='избранное резюме')),
            ],
            options={
                'verbose_name_plural': 'Избранные резюме',
            },
        ),
    ]

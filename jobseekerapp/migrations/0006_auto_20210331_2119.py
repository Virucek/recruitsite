# Generated by Django 3.1 on 2021-03-31 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0006_auto_20210331_2119'),
        ('jobseekerapp', '0005_auto_20210328_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritevacancies', to='employerapp.vacancy', verbose_name='Вакансия'),
        ),
    ]

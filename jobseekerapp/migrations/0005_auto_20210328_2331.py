# Generated by Django 3.1 on 2021-03-28 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0005_auto_20210325_2236'),
        ('authapp', '0001_initial'),
        ('jobseekerapp', '0004_favorite'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'vacancy')},
        ),
    ]

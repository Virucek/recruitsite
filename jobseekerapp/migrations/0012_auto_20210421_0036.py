# Generated by Django 3.1.1 on 2021-04-21 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekerapp', '0011_auto_20210420_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumeeducation',
            name='degree',
            field=models.CharField(choices=[('master', 'магистр'), ('bachelor', 'бакалавр'), ('specialist', 'специалист'), ('sertificate', 'сертификат')], default='master', max_length=64, null=True, verbose_name='Уровень'),
        ),
    ]

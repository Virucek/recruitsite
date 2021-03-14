# Generated by Django 3.1.1 on 2021-03-12 00:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_name', models.CharField(max_length=128, verbose_name='название вакансии')),
                ('city', models.CharField(max_length=64, verbose_name='город')),
                ('vacancy_type', models.CharField(choices=[('полная занятость', 'полная занятость'), ('частичная занятость', 'частичная занятость'), ('занятость по проекту', 'занятость по проекту'), ('удаленная работа', 'удаленная работа')], default='полная занятость', max_length=32, verbose_name='тип занятости')),
                ('min_salary', models.CharField(blank=True, help_text='поле необязательное для заполнения', max_length=32, verbose_name='минимальный уровень з/п')),
                ('max_salary', models.CharField(blank=True, help_text='поле необязательное для заполнения', max_length=32, verbose_name='максимальный уровень з/п')),
                ('currency', models.CharField(blank=True, choices=[('руб.', 'руб.'), ('USD', 'USD')], help_text='поле необязательное для заполнения', max_length=4, verbose_name='валюта')),
                ('description', models.TextField(max_length=264, verbose_name='описание / обязанности')),
                ('requirements', models.TextField(max_length=264, verbose_name='требования к кандидату')),
                ('conditions', models.TextField(blank=True, help_text='поле необязательное для заполнения', max_length=264, verbose_name='что мы предлагаем')),
                ('published', models.DateField(default=datetime.datetime.now, verbose_name='дата публикации')),
                ('contact_person', models.CharField(max_length=128, verbose_name='контактное лицо')),
                ('contact_email', models.EmailField(blank=True, help_text='поле необязательное', max_length=254, verbose_name='контактная почта')),
                ('hide', models.BooleanField(default=False, verbose_name='вакансия удалена / скрыта')),
                ('action', models.CharField(choices=[('draft', 'черновик'), ('need_moderation', 'требуется модерация'), ('moderation_ok', 'модерация пройдена успешно'), ('moderation_reject', 'отклонено модератором')], max_length=64, verbose_name='статус вакансии')),
                ('failed_moderation', models.TextField(blank=True, max_length=254, verbose_name='Сообщение в случае непрохождения модерации вакансии')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.employer')),
            ],
            options={
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]

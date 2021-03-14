from datetime import datetime

from django.db import models

from authapp.models import Employer


class Vacancy(models.Model):
    RUB = 'руб.'
    USD = 'USD'
    CURRENCY_CHOICE = (
        (RUB, 'руб.'),
        (USD, 'USD')
    )
    FULL = 'полная занятость'
    PART = 'частичная занятость'
    PRJ = 'занятость по проекту'
    REM = 'удаленная работа'
    TYPE_VACANCY = (
        (FULL, 'полная занятость'),
        (PART, 'частичная занятость'),
        (PRJ, 'занятость по проекту'),
        (REM, 'удаленная работа')
    )
    vacancy_name = models.CharField(verbose_name='название вакансии', max_length=128)
    city = models.CharField(verbose_name='город', max_length=64)
    vacancy_type = models.CharField(verbose_name='тип занятости', max_length=32,
                                    choices=TYPE_VACANCY, default=FULL)
    min_salary = models.CharField(verbose_name='минимальный уровень з/п', max_length=32, blank=True,
                              help_text='поле необязательное для заполнения')
    max_salary = models.CharField(verbose_name='максимальный уровень з/п', max_length=32,
                                  blank=True, help_text='поле необязательное для заполнения')
    currency = models.CharField(verbose_name='валюта', max_length=4, blank=True,
                                choices=CURRENCY_CHOICE, help_text='поле необязательное для '
                                                                   'заполнения')
    description = models.TextField(verbose_name='описание / обязанности', max_length=264)
    requirements = models.TextField(verbose_name='требования к кандидату', max_length=264)
    conditions = models.TextField(verbose_name='что мы предлагаем', max_length=264, blank=True,
                                  help_text='поле необязательное для заполнения')
    published = models.DateField(verbose_name='дата публикации', default=datetime.now)
    contact_person = models.CharField(verbose_name='контактное лицо', max_length=128)
    contact_email = models.EmailField(verbose_name='контактная почта', blank=True,
                                      help_text='поле необязательное')
    hide = models.BooleanField(verbose_name='вакансия удалена / скрыта', default=False)
    action = models.CharField(verbose_name='статус вакансии', max_length=64, choices=Employer.EMPLOYER_STATUS_CHOICES)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    failed_moderation = models.TextField(verbose_name='Сообщение в случае непрохождения '
                                            'модерации вакансии', max_length=254, blank=True)

    def __str__(self):
        return f'{self.vacancy_name} ({self.employer.company_name})'

    class Meta:
        verbose_name_plural = 'Вакансии'

    def save(self, *args, **kwargs):
        if self.action == 'moderation_ok' or self.action == 'moderation_reject':
            self.published = datetime.now()
        super(Vacancy, self).save(*args, **kwargs)

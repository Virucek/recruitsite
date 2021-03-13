from django.contrib.auth.models import User
from django.db import models

from authapp.models import Jobseeker


class Resume(models.Model):
    DRAFT = 'draft'
    OPENED = 'opened'
    RESUME_STATUS_CHOICES = (
        (DRAFT, 'черновик'),
        (OPENED, 'открыт'),
    )

    name = models.CharField(verbose_name='Желаемая должность', max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salary_min = models.IntegerField(verbose_name='Минимальная зарплата', blank=True)
    salary_max = models.IntegerField(verbose_name='Максимальная зарплата', blank=True)
    currency = models.CharField(verbose_name='Валюта', max_length=3, blank=True)
    added_at = models.DateTimeField(verbose_name='Время добавления резюме', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время обновления резюме', auto_now=True)
    key_skills = models.CharField(verbose_name='Ключевые навыки', max_length=256, blank=True)
    about = models.TextField(verbose_name='О себе', blank=True)
    status = models.CharField(verbose_name='Статус', choices=RESUME_STATUS_CHOICES, max_length=16)
    is_active = models.BooleanField(verbose_name='Активный', default=True)


class ResumeEducation(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме')
    edu_type = models.CharField(verbose_name='Тип образования', max_length=32)
    degree = models.CharField(verbose_name='Степень', max_length=64)
    institution_name = models.CharField(verbose_name='Название учреждения', max_length=64)
    from_date = models.DateField(verbose_name='Начало периода')
    to_date = models.DateField(verbose_name='Конец периода', blank=True)
    course_name = models.CharField(verbose_name='Название курса/кафедры', max_length=256)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)


class ResumeExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Название компании', max_length=128)
    from_date = models.DateField(verbose_name='Начало работы')
    to_date = models.DateField(verbose_name='Конец работы', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

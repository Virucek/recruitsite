from datetime import date

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
    salary_min = models.IntegerField(verbose_name='Минимальная зарплата', blank=True, null=True)
    salary_max = models.IntegerField(verbose_name='Максимальная зарплата', blank=True, null=True)
    currency = models.CharField(verbose_name='Валюта', max_length=3, blank=True, null=True)
    added_at = models.DateTimeField(verbose_name='Время добавления резюме', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время обновления резюме', auto_now=True)
    key_skills = models.TextField(verbose_name='Ключевые навыки', blank=True, null=True)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    status = models.CharField(verbose_name='Статус', choices=RESUME_STATUS_CHOICES, max_length=16, default=OPENED)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name_plural = verbose_name = 'Резюме'

    def __str__(self):
        return f'{self.name} {self.user.first_name} {self.user.last_name}'

    def get_experience_items(self):
        return self.experienceitems.select_related().filter(is_active=True)

    def get_education_items(self):
        return self.educationitems.select_related().filter(is_active=True)

    @staticmethod
    def get_user_resumes(user_id):
        return Resume.objects.filter(is_active=True, user_id=user_id)


class ResumeEducation(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме', related_name='educationitems')
    HIGH = 'high'
    ONLINE = 'online'
    EDU_TYPE_CHOICES = (
        ('high', 'высшее'),
        ('online', 'онлайн-курсы'),
    )
    edu_type = models.CharField(verbose_name='Тип образования', max_length=32, choices=EDU_TYPE_CHOICES, blank=False, default=HIGH)
    MASTER = 'master'
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    SERTIFICATE = 'sertificate'
    DEGREE_CHOICES = (
        (MASTER, 'магистр'),
        (BACHELOR, 'бакалавр'),
        (SPECIALIST, 'специлист'),
        (SERTIFICATE, 'сертификат'),
    )
    degree = models.CharField(verbose_name='Уровень', max_length=64, null=True, choices=DEGREE_CHOICES, blank=False, default=MASTER)
    institution_name = models.CharField(verbose_name='Название учреждения', max_length=64)
    from_date = models.DateField(verbose_name='Начало периода', blank=True, null=True)
    to_date = models.DateField(verbose_name='Конец периода(фактическая или планируемая)')
    course_name = models.CharField(verbose_name='Название курса/кафедры', max_length=256)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name = 'Место обучения для резюме'
        verbose_name_plural = 'Места обучения для резюме'

    def __str__(self):
        return f'{self.resume.name} {self.resume.user.first_name} {self.resume.user.last_name} ' \
               f'({self.get_edu_type_display()}, {self.get_degree_display()})'


class ResumeExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experienceitems')
    company_name = models.CharField(verbose_name='Название компании', max_length=128)
    job_title = models.CharField(verbose_name='Название вакансии', max_length=128)
    from_date = models.DateField(verbose_name='Начало работы')
    to_date = models.DateField(verbose_name='Конец работы', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name = 'Место опыта для резюме'
        verbose_name_plural = 'Места опыта для резюме'

    def __str__(self):
        return f'{self.resume.name} {self.resume.user.first_name} {self.resume.user.last_name} {self.company_name} ' \
               f'{self.job_title}'

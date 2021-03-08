from django.contrib.auth.models import User
from django.db import models


class Employer(models.Model):
    company_name = models.CharField(verbose_name='название компании', max_length=256, unique=True)
    tax_number = models.CharField(verbose_name='ИНН компании', max_length=16, blank=True)
    phone_number = models.CharField(verbose_name='телефон', max_length=11, blank=True)
    site = models.CharField(verbose_name='сайт компании', max_length=32, blank=True)
    industry_type = models.CharField(verbose_name='тип отрасли компании', max_length=32, blank=True)
    short_description = models.TextField(verbose_name='краткое описание компании', blank=True)
    logo = models.ImageField(upload_to='company_logo', blank=True)
    city = models.CharField(verbose_name='город расположения компании', max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.company_name


class Jobseeker(models.Model):
    GENDER_CHOICES = (
        ('m', 'мужской'),
        ('f', 'женский'),
    )
    MARRIED_STATUS_CHOICES = (
        ('h', 'холост'),
        ('m', 'замужем/женат'),
        ('d', 'разведен/разведена'),
    )
    middle_name = models.CharField(verbose_name='отчество', max_length=32)
    gender = models.CharField(verbose_name='пол', max_length=16, choices=GENDER_CHOICES)
    birthday = models.DateField(verbose_name='дата рождения', null=True, blank=True)
    city = models.CharField(verbose_name='город', max_length=64)
    married_status = models.CharField(verbose_name='Статус в браке', max_length=1, choices=MARRIED_STATUS_CHOICES)
    photo = models.ImageField(upload_to='jobseeker_photo', blank=True)
    phone_number = models.CharField(verbose_name='телефон', max_length=11)
    about = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

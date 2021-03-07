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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

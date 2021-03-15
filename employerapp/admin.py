from datetime import datetime

from django.contrib import admin

from employerapp.models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('vacancy_name', 'employer', 'action',)
    list_filter = ('action', )





from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.models import Employer, IndustryType
from employerapp.forms import VacancyCreationForm, VacancyEditForm
from employerapp.models import Vacancy
from jobseekerapp.models import Resume


@login_required
def employer_cabinet(request, emp_id):
    title = 'Личный кабинет работодателя'
    employer = get_object_or_404(Employer, pk=emp_id)
    industry_type = IndustryType.objects.get(id=employer.industry_type_id)
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False,employer=employer).order_by('published')
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(
        action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    content = {
        'title': title,
        'employer': employer,
        'industry_type': industry_type.descx,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all
    }
    return render(request, 'employerapp/employer_cabinet.html', content)


@login_required
def vacancy_published(request, emp_id):
    title = 'Опубликованные вакансии'
    employer = get_object_or_404(Employer, pk=emp_id)
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by(
        'published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False,
                                       employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    context = {
        'title': title,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all
    }

    return render(request, 'employerapp/vacancy_published.html', context)


@login_required
def vacancy_draft(request, emp_id):
    employer = get_object_or_404(Employer, pk=emp_id)
    title = 'Черновики'
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by(
        'published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False, employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    context = {
        'title': title,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all
    }

    return render(request, 'employerapp/vacancy_drafts.html', context)


@login_required
def vacancy_hide(request, emp_id):
    employer = get_object_or_404(Employer, pk=emp_id)
    title = 'Удаленные вакансии'
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False, employer=employer).order_by(
        'published')
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all
    }

    return render(request, 'employerapp/vacancy_hide.html', context)


@login_required
def messages(request, emp_id):
    title = 'Сообщения от админа портала'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False, employer=employer).order_by(
        'published')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all
    }

    return render(request, 'employerapp/employer_messages.html', context)


def vacancy_create(request, emp_id):
    employer = get_object_or_404(Employer, pk=emp_id)
    title = 'создание вакансии'
    sent = False
    action = None
    if request.method == 'POST':
        form = VacancyCreationForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.action = form.cleaned_data.get('action')
            vacancy.city = form.cleaned_data.get('city')
            vacancy.vacancy_name = form.cleaned_data.get('vacancy_name')
            vacancy.min_salary = form.cleaned_data.get('min_salary')
            vacancy.max_salary = form.cleaned_data.get('max_salary')
            vacancy.currency = form.cleaned_data.get('currency')
            vacancy.requirements = form.cleaned_data.get('requirements')
            vacancy.description = form.cleaned_data.get('description')
            vacancy.conditions = form.cleaned_data.get('conditions')
            vacancy.contact_email = form.cleaned_data.get('contact_email')
            vacancy.contact_person = form.cleaned_data.get('contact_person')
            vacancy.vacancy_type = form.cleaned_data.get('vacancy_type')
            vacancy.employer = employer
            vacancy.save()
            sent = True
            action = vacancy.action
    else:
        form = VacancyCreationForm()
    context = {'title': title, 'form': form, 'sent': sent, 'employer': employer, 'action': action}

    return render(request, 'employerapp/vacancy_creation.html', context)


@login_required
def vacancy_edit_draft(request, emp_id, pk):
    title = 'Редактирование вакансии'
    vacancy = get_object_or_404(Vacancy, pk=pk)
    employer = get_object_or_404(Employer, pk=emp_id)
    sent = False
    if request.method == 'POST':
        form = VacancyCreationForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            sent = True
    else:
        form = VacancyCreationForm(instance=vacancy)

    context = {'title': title, 'form': form, 'sent': sent, 'employer': employer, 'vacancy': vacancy}

    return render(request, 'employerapp/vacancy_edit.html', context)


@login_required
def vacancy_edit(request, emp_id, pk):
    title = 'Редактирование вакансии'
    vacancy = get_object_or_404(Vacancy, pk=pk)
    employer = get_object_or_404(Employer, pk=emp_id)
    sent = False
    if request.method == 'POST':
        form = VacancyEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            sent = True
    else:
        form = VacancyEditForm(instance=vacancy)

    context = {'title': title, 'form': form, 'sent': sent, 'employer': employer, 'vacancy': vacancy}

    return render(request, 'employerapp/vacancy_edit.html', context)


@login_required
def vacancy_delete(request, emp_id, pk):
    title = 'Удаление вакансии'
    employer = get_object_or_404(Employer, pk=emp_id)
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST' and (vacancy.employer.DRAFT or vacancy.employer.MODER_OK):
        if not vacancy.hide:
            vacancy.hide = True
        else:
            vacancy.hide = False
        vacancy.save()
        return HttpResponseRedirect(reverse('employer:main', args=[vacancy.employer.pk]))

    context = {'title': title, 'vacancy_delete': vacancy, 'employer': employer}

    return render(request, 'employerapp/vacancy_delete.html', context)


@login_required
def vacancy_view(request, emp_id, pk):
    title = 'Вакансия'
    vacancy = get_object_or_404(Vacancy, pk=pk)
    employer = get_object_or_404(Employer, pk=emp_id)

    context = {'title': title, 'item': vacancy, 'employer': employer}

    return render(request, 'employerapp/vacancy_view.html', context)

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.models import Employer, IndustryType, Jobseeker
from employerapp.forms import VacancyCreationForm, VacancyEditForm, SendOfferForm
from employerapp.models import Vacancy, SendOffers, Favorites
from jobseekerapp.models import Resume, Offer


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
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    responses = Offer.objects.filter(vacancy__employer=employer.pk, direction='O').order_by('date')
    content = {
        'title': title,
        'employer': employer,
        'industry_type': industry_type.descx,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'favorites': favorites,
        'responses': responses
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
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    responses = Offer.objects.filter(vacancy__employer=employer.pk, direction='O').order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'favorites': favorites,
        'responses': responses
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
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    responses = Offer.objects.filter(vacancy=employer.pk, direction='O').order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'drafts': drafts,
        'vacancies_hide': vacancies_hide,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'favorites': favorites,
        'responses': responses
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
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    responses = Offer.objects.filter(vacancy__employer=employer.pk, direction='O').order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'favorites': favorites,
        'responses': responses
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
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    responses = Offer.objects.filter(vacancy__employer=employer.pk, direction='O').order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'favorites': favorites,
        'responses': responses
    }

    return render(request, 'employerapp/employer_messages.html', context)


@login_required
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

    context = {'title': title, 'item': vacancy, 'employer': employer, 'user': request.user.id}

    return render(request, 'employerapp/vacancy_view.html', context)


@login_required
def send_offer(request, emp_id, pk):
    title = 'Предложение по работе'
    employer = get_object_or_404(Employer, pk=emp_id)
    resume = get_object_or_404(Resume, pk=pk)

    sent = False
    if request.method == 'POST':
        form = SendOfferForm(request.POST, employer=employer)
        send = SendOffers()
        jobseeker_offer = Offer()

        if form.is_valid():
            send.vacancy = jobseeker_offer.vacancy = form.cleaned_data.get('vacancy')
            send.cover_letter = jobseeker_offer.cover_letter = form.cleaned_data.get('cover_letter')
            send.contact_phone = jobseeker_offer.contact_phone = form.cleaned_data.get('contact_phone')
            send.resume = jobseeker_offer.resume = resume
            jobseeker_offer.direction = Offer.INCOMING
            send.save()
            jobseeker_offer.save()
            sent = True
    else:
        form = SendOfferForm(employer=employer)

    context = {'title': title, 'employer': employer, 'sent': sent, 'form': form}

    return render(request, 'employerapp/send_offer.html',  context)


@login_required
def favorites(request, emp_id):
    title = 'Избранные резюме'
    employer = get_object_or_404(Employer, pk=emp_id)
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(
        action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False,
                                       employer=employer).order_by(
        'published')
    responses = Offer.objects.filter(vacancy__employer=employer.pk, direction='O').order_by('date')
    context = {
        'title': title,
        'employer': employer,
        'favorites': favorites,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
        'responses': responses
    }
    return render(request, 'employerapp/favorites.html', context)


@login_required
def delete_favorite(request, emp_id, pk):
    title = 'Удаление избранных резюме'
    employer = get_object_or_404(Employer, pk=emp_id)
    favorite = get_object_or_404(Favorites, pk=pk)
    if request.method == 'POST':
        favorite.delete()
        return HttpResponseRedirect(reverse('employer:favorites', args=[employer.pk]))

    context = {'title': title, 'favorite': favorite, 'employer': employer}

    return render(request, 'employerapp/delete_favorite.html', context)


@login_required
def search_resume(request, emp_id):
    title = 'Поиск резюме'
    employer = get_object_or_404(Employer, pk=emp_id)
    search = request.GET.get('search')
    search_paginator = None
    if search:
        query = []
        results = Resume.objects.filter(Q(name__icontains=search) | Q(key_skills__icontains=search)).filter(
            status=Resume.OPENED).order_by('-updated_at')
        query.append(results)
        query = list(chain(*query))

        page = request.GET.get('page')
        paginator = Paginator(query, 5)
        try:
            search_paginator = paginator.page(page)
        except PageNotAnInteger:
            search_paginator = paginator.page(1)
        except EmptyPage:
            search_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'object_list': search_paginator, 'search': search}

    return render(request, 'employerapp/search_resume.html', context)


@login_required
def responses(request, emp_id):
    title = 'Отклики по вакансиям'
    employer = get_object_or_404(Employer, pk=emp_id)
    responses = Offer.objects.filter(vacancy__employer=employer.pk, direction='O').order_by(
        'date')
    favorites = Favorites.objects.filter(employer=employer).order_by('date')
    vacancies_all = Vacancy.objects.filter(employer=employer).exclude(
        action=employer.NEED_MODER).exclude(action=employer.DRAFT).order_by('published')
    vacancies_hide = Vacancy.objects.filter(hide=True, employer=employer).order_by(
        'published')
    drafts = Vacancy.objects.filter(action=employer.DRAFT, hide=False, employer=employer).order_by(
        'published')
    vacancies = Vacancy.objects.filter(action=employer.MODER_OK, hide=False,
                                       employer=employer).order_by(
        'published')
    context = {
        'title': title,
        'employer': employer,
        'responses': responses,
        'favorites': favorites,
        'vacancies_hide': vacancies_hide,
        'drafts': drafts,
        'vacancies': vacancies,
        'vacancies_all': vacancies_all,
    }

    return render(request, 'employerapp/employer_responses.html', context)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
<<<<<<< HEAD

from authapp.models import Employer
from employerapp.models import Vacancy
=======
from django.contrib.auth.decorators import login_required

from authapp.models import Employer
from employerapp.models import Vacancy
from jobseekerapp.models import Resume
>>>>>>> sprint2_vacations
from mainapp.models import News


def main(request, page=None):
    title = 'Главная'
    if page is None:
        page = 1
        return HttpResponseRedirect(reverse('main', kwargs={'page': page}))
    news = News.objects.filter(is_active=True).order_by('-published')
    employers = Employer.objects.filter(is_active=True, status=Employer.MODER_OK).order_by('?')[:6]
    vacancies = Vacancy.objects.filter(action='moderation_ok')
    paginator = Paginator(news, 4)
    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)
<<<<<<< HEAD
=======

    resume_all = Resume.objects.all().filter(status='opened').order_by('updated_at')

>>>>>>> sprint2_vacations
    context = {
        'title': title,
        'news': news_paginator,
        'employers': employers,
<<<<<<< HEAD
        'vacancies': vacancies
=======
        'vacancies': vacancies,
        'resume_all': resume_all
>>>>>>> sprint2_vacations
    }
    return render(request, 'mainapp/index.html', context)


def news_detail(request, pk):
    one_news = News.objects.get(pk=pk)
    title = one_news.pk
    context = {
        'title': title,
        'one_news': one_news
    }
    return render(request, 'mainapp/news_detail.html', context)

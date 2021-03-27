from itertools import chain

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import Employer
from employerapp.models import Vacancy, Favorites
from django.contrib.auth.decorators import login_required

from authapp.models import Employer
from employerapp.models import Vacancy
from jobseekerapp.models import Resume
from mainapp.models import News


def main(request, page=None):
    title = 'Главная'
    if page is None:
        page = 1
        return HttpResponseRedirect(reverse('main', kwargs={'page': page}))
    news = News.objects.filter(is_active=True).order_by('-published')
    employers = Employer.objects.filter(is_active=True, status=Employer.MODER_OK).order_by('?')[:6]
    vacancies = Vacancy.objects.filter(action='moderation_ok')
    resume_all = Resume.objects.all().filter(status='opened').order_by('updated_at')
    paginator = Paginator(news, 4)
    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)

    favorites = Favorites()
    if request.method == 'POST' and request.user.employer:
        resume = Resume.objects.get(pk=int(request.POST.get('checked')))
        favorites.resume = resume
        favorites.employer = request.user.employer
        if not Favorites.objects.filter(resume=resume,
                                        employer=request.user.employer).first():
            favorites.save()

    context = {
        'title': title,
        'news': news_paginator,
        'employers': employers,
        'vacancies': vacancies,
        'resume_all': resume_all
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


def search_news(request):
    title = 'Поиск новостей'
    search = request.GET.get('search')
    search_paginator = None
    if search:
        query = []
        results = News.objects.filter(Q(title__icontains=search) | Q(description__icontains=search), is_active=True).order_by(
            '-published')
        query.append(results)
        query = list(chain(*query))

        page = request.GET.get('page')
        paginator = Paginator(query, 3)
        try:
            search_paginator = paginator.page(page)
        except PageNotAnInteger:
            search_paginator = paginator.page(1)
        except EmptyPage:
            search_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'search_news': search_paginator, 'search': search}

    return render(request, 'mainapp/search_news.html', context)

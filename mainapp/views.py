from django.shortcuts import render

from authapp.models import Employer
from mainapp.models import News


def main(request):
    title = 'Главная'
    news = News.objects.filter(is_active=True).order_by('-published')
    employers = Employer.objects.filter(is_active=True, status=Employer.MODER_OK)[:5]
    context = {
        'title': title,
        'news': news,
        'employers': employers,
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

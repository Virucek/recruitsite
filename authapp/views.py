from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import UserLoginForm, EmployerRegisterForm
from authapp.models import Employer


def login(request):
    title = 'вход'

    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
    }
    return render(request, 'authapp/login.html', context=content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register_employer(request):
    title = 'Регистрация работодателя'

    if request.method == 'POST':
        register_form = EmployerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            employer = Employer.objects.create(user=user)
            employer.company_name = register_form.cleaned_data.get('company_name')
            employer.tax_number = register_form.cleaned_data.get('tax_number')
            employer.phone_number = register_form.cleaned_data.get('phone_number')
            employer.site = register_form.cleaned_data.get('site')
            employer.industry_type = register_form.cleaned_data.get('industry_type')
            employer.short_description = register_form.cleaned_data.get('short_description')
            employer.logo = register_form.cleaned_data.get('logo')
            employer.city = register_form.cleaned_data.get('city')

            employer.save()

            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = EmployerRegisterForm()

    content = {
        'title': title,
        'register_form': register_form,
    }
    return render(request, 'authapp/register_employer.html', context=content)

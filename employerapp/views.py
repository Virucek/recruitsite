from django.shortcuts import render
from authapp.models import Employer

def employer_cabinet(request):
    title = 'Личный кабинет работодателя'
    current_user = request.user.id
    employer_data = Employer.objects.get(user_id=current_user)
    content = {'title': title, 'employer': employer_data}
    return render(request, 'employerapp/employer_cabinet.html', content)

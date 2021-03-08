from django.shortcuts import render
from authapp.models import Employer, IndustryType

def employer_cabinet(request):
    title = 'Личный кабинет работодателя'
    current_user = request.user.id
    employer_data = Employer.objects.get(user_id=current_user)
    industry_type = IndustryType.objects.get(id=employer_data.industry_type_id)
    content = {'title': title, 'employer': employer_data, 'industry_type':industry_type.descx}
    return render(request, 'employerapp/employer_cabinet.html', content)


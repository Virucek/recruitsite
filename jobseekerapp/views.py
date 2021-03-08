from django.shortcuts import render
from authapp.models import Jobseeker

def jobseeker_cabinet(request):
    title = 'Личный кабинет работодателя'
    current_user = request.user.id
    jobseeker_data = Jobseeker.objects.get(user_id=current_user)
    content = {'title': title, 'jobseeker': jobseeker_data}
    return render(request, 'jobseekerapp/jobseeker_cabinet.html', content)


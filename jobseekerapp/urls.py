from django.urls import path

from jobseekerapp import views

app_name = 'jobseekerapp'

urlpatterns = [
    path('', views.jobseeker_cabinet, name='cabinet'),
    path('resume/', views.ResumeCreateView.as_view(), name='resume'),
]
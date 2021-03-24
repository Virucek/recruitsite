from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/employer/', authapp.register_employer, name='register_employer'),
    path('register/jobseeker/', authapp.register_jobseeker, name='register_jobseeker'),
    path('edit/', authapp.edit, name='edit'),
    path('jobseeker/<int:pk>/edit/', authapp.JobseekerUpdateView.as_view(), name='edit_jobseeker'),
]

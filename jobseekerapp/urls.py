from django.urls import path

from jobseekerapp import views

app_name = 'jobseekerapp'

urlpatterns = [
    path('', views.jobseeker_cabinet, name='cabinet'),
    path('resume/', views.ResumeCreateView.as_view(), name='resume'),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume_detail'),
    path('resume/<int:pk>/edit', views.ResumeUpdateView.as_view(), name='resume_update'),
    path('resume/<int:pk>/delete', views.ResumeDeleteView.as_view(), name='resume_delete'),
    path('resume/<int:resume_id>/experience', views.ResumeExperienceCreateView.as_view(), name='resume_experience'),
    path('resume/<int:resume_id>/experience/<int:pk>/edit', views.ResumeExperienceUpdateView.as_view(), name='resume_experience_update'),
    path('resume/<int:resume_id>/experience/<int:pk>/delete', views.ResumeExperienceDeleteView.as_view(), name='resume_experience_delete'),
    path('resume/<int:resume_id>/education', views.ResumeEducationCreateView.as_view(), name='resume_education'),
    path('resume/<int:resume_id>/education/<int:pk>/edit', views.ResumeEducationUpdateView.as_view(), name='resume_education_update'),
    path('resume/<int:resume_id>/education/<int:pk>/delete', views.ResumeEducationDeleteView.as_view(), name='resume_education_delete'),
]
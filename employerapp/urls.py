from django.urls import path

from employerapp import views

app_name = 'employerapp'

urlpatterns = [
    path('<int:emp_id>/', views.employer_cabinet, name='main'),
    path('<int:emp_id>/drafts/', views.vacancy_draft, name='drafts'),
    path('<int:emp_id>/published/', views.vacancy_published, name='published'),
    path('<int:emp_id>/messages/', views.messages, name='messages'),
    path('<int:emp_id>/hide/', views.vacancy_hide, name='hide'),
    path('<int:emp_id>/vacancy_create/', views.vacancy_create, name='vacancy_create'),
    path('<int:emp_id>/vacancy_draft_edit/<int:pk>/', views.vacancy_edit_draft,
         name='vacancy_edit_draft'),
    path('<int:emp_id>/vacancy_edit/<int:pk>/', views.vacancy_edit, name='vacancy_edit'),
    path('<int:emp_id>/vacancy_delete/<int:pk>/', views.vacancy_delete, name='vacancy_delete'),
    path('<int:emp_id>/vacancy_view/<int:pk>/', views.vacancy_view, name='vacancy_view')
]
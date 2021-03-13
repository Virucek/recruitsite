from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authapp.models import Jobseeker
from jobseekerapp.forms import ResumeEducationForm, ResumeExperienceForm
from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience


def jobseeker_cabinet(request):
    title = 'Личный кабинет работодателя'
    current_user = request.user.id
    jobseeker_data = Jobseeker.objects.get(user_id=current_user)
    content = {'title': title, 'jobseeker': jobseeker_data}
    return render(request, 'jobseekerapp/jobseeker_cabinet.html', content)


class ResumeCreateView(CreateView):
    model = Resume
    template_name = 'jobseekerapp/resume_create.html'
    fields = [
        'name',
        'salary_min',
        'salary_max',
        'currency',
        'key_skills',
        'about',
    ]
    success_url = reverse_lazy('jobseeker:cabinet')

    def get_context_data(self, **kwargs):
        data = super(ResumeCreateView, self).get_context_data(**kwargs)
        EducationFormSet = inlineformset_factory(Resume, ResumeEducation, ResumeEducationForm, extra=1)
        education_formset = EducationFormSet(self.request.POST) if self.request.POST else EducationFormSet()

        data['education_items'] = education_formset

        ExperienceFormSet = inlineformset_factory(Resume, ResumeExperience, ResumeExperienceForm, extra=1)
        experience_formset = ExperienceFormSet(self.request.POST) if self.request.POST else ExperienceFormSet()

        data['experience_items'] = experience_formset
        print(data)

        return data

    # @login_required
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        education_items = context['education_items']
        with transaction.atomic():
            self.object = form.save()
            if education_items.is_valid():
                education_items.instance = self.object
                education_items.save()

        experience_items = context['experience_items']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if experience_items.is_valid():
                experience_items.instance = self.object
                experience_items.save()

        return super(ResumeCreateView, self).form_valid(form)


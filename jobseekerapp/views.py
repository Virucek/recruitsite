from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from authapp.models import Jobseeker
from jobseekerapp.forms import ResumeEducationForm, ResumeExperienceForm, ResumeForm
from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience


class JobseekerViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['title'] = getattr(self, 'title')
        except AttributeError:
            print("title for view isn't set")
            context['title'] = 'Untitled page'

        return context

    def dispatch(self, request, *args, **kwargs):
        disp = super().dispatch
        decorators = getattr(self, 'decorators', [login_required])

        for decorator in decorators:
            disp = decorator(disp)

        return disp(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ResumeItemViewMixin(JobseekerViewMixin):

    def get_success_url(self):
        resume_id = self.kwargs['resume_id']
        return reverse_lazy('jobseeker:resume_detail', kwargs={'pk': resume_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_id = self.kwargs['resume_id']
        context['resume'] = Resume.objects.get(pk=resume_id)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.resume = context['resume']
        self.object = form.save

        return super().form_valid(form)


def jobseeker_cabinet(request):
    title = 'Личный кабинет работодателя'
    current_user = request.user.id
    jobseeker_data = Jobseeker.objects.get(user_id=current_user)
    content = {'title': title, 'jobseeker': jobseeker_data}
    return render(request, 'jobseekerapp/jobseeker_cabinet.html', content)


class ResumeCreateView(JobseekerViewMixin, CreateView):
    model = Resume
    template_name = 'jobseekerapp/resume_create.html'
    form_class = ResumeForm
    success_url = reverse_lazy('jobseeker:cabinet')
    title = 'Создание резюме'

    def get_success_url(self):
        data = self.get_context_data()
        return reverse_lazy('jobseeker:resume_detail', kwargs={'pk': data['resume'].id})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'salary_min' not in form.cleaned_data and 'salary_max' not in form.cleaned_data:
            form.cleaned_data.pop('currency')
        self.object = form.save

        return super(ResumeCreateView, self).form_valid(form)


class ResumeDetailView(JobseekerViewMixin, DetailView):
    model = Resume
    template_name = 'jobseekerapp/resume_detail.html'
    title = 'Просмотр резюме'


class ResumeUpdateView(JobseekerViewMixin, UpdateView):
    model = Resume
    template_name = 'jobseekerapp/resume_create.html'
    success_url = reverse_lazy('jobseeker:cabinet')
    form_class = ResumeForm
    title = 'Редактирование резюме'


class ResumeDeleteView(JobseekerViewMixin, DeleteView):
    model = Resume
    template_name = 'jobseekerapp/resume_delete.html'
    success_url = reverse_lazy('jobseeker:cabinet')
    title = 'Удаление резюме'


class ResumeExperienceCreateView(ResumeItemViewMixin, CreateView):
    model = ResumeExperience
    template_name = 'jobseekerapp/resume_experience_create.html'
    form_class = ResumeExperienceForm
    title = 'Добавление записи об опыте'


class ResumeExperienceUpdateView(ResumeItemViewMixin, UpdateView):
    model = ResumeExperience
    template_name = 'jobseekerapp/resume_experience_create.html'
    form_class = ResumeExperienceForm
    title = 'Редактирование записи об опыте'


class ResumeExperienceDeleteView(ResumeItemViewMixin, DeleteView):
    model = ResumeExperience
    template_name = 'jobseekerapp/resume_experience_delete.html'
    title = 'Удаление записи об опыте'

    def get_success_url(self):
        resume_id = self.kwargs['resume_id']
        return reverse_lazy('jobseeker:resume_detail', kwargs={'pk': resume_id})


class ResumeEducationCreateView(ResumeItemViewMixin, CreateView):
    model = ResumeEducation
    template_name = 'jobseekerapp/resume_education_create.html'
    form_class = ResumeEducationForm
    title = 'Добавление записи об обучении'


class ResumeEducationUpdateView(ResumeItemViewMixin, UpdateView):
    model = ResumeEducation
    template_name = 'jobseekerapp/resume_education_create.html'
    form_class = ResumeEducationForm
    title = 'Редактирование записи об обучении'


class ResumeEducationDeleteView(ResumeItemViewMixin, DeleteView):
    model = ResumeEducation
    template_name = 'jobseekerapp/resume_education_delete.html'
    title = 'Удаление записи об обучении'

    def get_success_url(self):
        resume_id = self.kwargs['resume_id']
        return reverse_lazy('jobseeker:resume_detail', kwargs={'pk': resume_id})



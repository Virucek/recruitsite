from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from authapp.models import Jobseeker
from employerapp.models import Favorites
from employerapp.models import Vacancy
from jobseekerapp.forms import ResumeEducationForm, ResumeExperienceForm, ResumeForm, JobseekerOfferForm
from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience, Offer


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
        jobseeker_id = self.kwargs['jobseeker_id']
        return reverse_lazy('jobseeker:resume_detail', kwargs={'jobseeker_id': jobseeker_id, 'pk': resume_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_id = self.kwargs['resume_id']
        context['resume'] = Resume.objects.get(pk=resume_id)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.resume = context['resume']
        self.object = form.save()

        return super().form_valid(form)


class JobseekerDetailView(JobseekerViewMixin, DetailView):
    model = Resume
    template_name = 'jobseekerapp/jobseeker_cabinet.html'
    title = 'Личный кабинет соискателя'

    def get_object(self, queryset=None):
        return Jobseeker.objects.get(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(JobseekerDetailView, self).get_context_data()
        context['resumes'] = Resume.get_user_resumes(self.request.user.id)
        return context


class ResumeCreateView(JobseekerViewMixin, CreateView):
    """
    Создание резюме.

    *Model*
    :model:`jobseekerapp.Resume`

    *Template*
    :template:`jobseekerapp/resume_create.html`
    """

    model = Resume
    template_name = 'jobseekerapp/resume_create.html'
    form_class = ResumeForm
    title = 'Создание резюме'

    def get_success_url(self):
        data = self.get_context_data()
        print(data)
        return reverse_lazy('jobseeker:resume_detail',
                            kwargs={'jobseeker_id': data['resume'].user.id, 'pk': data['resume'].id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'salary_min' not in form.cleaned_data and 'salary_max' not in form.cleaned_data:
            form.cleaned_data['currency'].pop()
        self.object = form.save()

        return super(ResumeCreateView, self).form_valid(form)


class ResumeDetailView(JobseekerViewMixin, DetailView):
    """
    Просмотр резюме.

    *Model*
    :model:`jobseekerapp.Resume`

    *Template*
    :template:`jobseekerapp/resume_detail.html`
    """

    model = Resume
    template_name = 'jobseekerapp/resume_detail.html'
    title = 'Резюме'


class ResumeUpdateView(JobseekerViewMixin, UpdateView):
    """
    Редактирование резюме.

    *Model*
    :model:`jobseekerapp.Resume`

    *Template*
    :template:`jobseekerapp/resume_create.html`
    """
    model = Resume
    template_name = 'jobseekerapp/resume_create.html'
    form_class = ResumeForm
    title = 'Редактирование резюме'

    def get_success_url(self):
        data = self.get_context_data()
        return reverse_lazy('jobseeker:resume_detail',
                            kwargs={'jobseeker_id': data['resume'].user.id, 'pk': data['resume'].id})


class ResumeDeleteView(JobseekerViewMixin, DeleteView):
    """
    Удаление резюме.

    *Model*
    :model:`jobseekerapp.Resume`

    *Template*
    :template:`jobseekerapp/resume_delete.html`
    """
    model = Resume
    template_name = 'jobseekerapp/resume_delete.html'
    title = 'Удаление резюме'

    def get_success_url(self):
        data = self.get_context_data()
        return reverse_lazy('jobseeker:cabinet', kwargs={'jobseeker_id': data['object'].user.id})


class ResumeExperienceCreateView(ResumeItemViewMixin, CreateView):
    """
    Добавление данных об опытке.

    *Model*
    :model:`jobseekerapp.ResumeExperience`

    *Template*
    :template:`jobseekerapp/resume_experience_create.html`
    """
    model = ResumeExperience
    template_name = 'jobseekerapp/resume_experience_create.html'
    form_class = ResumeExperienceForm
    title = 'Добавление записи об опыте'


class ResumeExperienceUpdateView(ResumeItemViewMixin, UpdateView):
    """
    Редактирование данных об опыте.

    *Model*
    :model:`jobseekerapp.ResumeExperience`

    *Template*
    :template:`jobseekerapp/resume_experience_create.html`
    """
    model = ResumeExperience
    template_name = 'jobseekerapp/resume_experience_create.html'
    form_class = ResumeExperienceForm
    title = 'Редактирование записи об опыте'


class ResumeExperienceDeleteView(ResumeItemViewMixin, DeleteView):
    """
    Удаление записи об опытке.

    *Model*
    :model:`jobseekerapp.ResumeExperience`

    *Template*
    :template:`jobseekerapp/resume_experience_delete.html`
    """
    model = ResumeExperience
    template_name = 'jobseekerapp/resume_experience_delete.html'
    title = 'Удаление записи об опыте'


class ResumeEducationCreateView(ResumeItemViewMixin, CreateView):
    """
    Добавление записи об обучении.

    *Model*
    :model:`jobseekerapp.ResumeEducation`

    *Template*
    :template:`jobseekerapp/resume_education_create.html`
    """
    model = ResumeEducation
    template_name = 'jobseekerapp/resume_education_create.html'
    form_class = ResumeEducationForm
    title = 'Добавление записи об обучении'


class ResumeEducationUpdateView(ResumeItemViewMixin, UpdateView):
    """
    Редактирование записи об обучении.

    *Model*
    :model:`jobseekerapp.ResumeEducation`

    *Template*
    :template:`jobseekerapp/resume_education_create.html`
    """
    model = ResumeEducation
    template_name = 'jobseekerapp/resume_education_create.html'
    form_class = ResumeEducationForm
    title = 'Редактирование записи об обучении'


class ResumeEducationDeleteView(ResumeItemViewMixin, DeleteView):
    """
    Удаление записи об обучении.

    *Model*
    :model:`jobseekerapp.ResumeEducation`

    *Template*
    :template:`jobseekerapp/resume_education_delete.html`
    """
    model = ResumeEducation
    template_name = 'jobseekerapp/resume_education_delete.html'
    title = 'Удаление записи об обучении'


class ResumeExternalDetailView(JobseekerViewMixin, DetailView):
    """
    Резюме расширенный просмотр.

    *Model*
    :model:`jobseekerapp.Resume`

    *Template*
    :template:`jobseekerapp/resume_external_detail.html`
    """
    model = Resume
    template_name = 'jobseekerapp/resume_external_detail.html'
    title = 'Резюме'

    def post(self, request, *args, **kwargs):
        favorites = Favorites()
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        favorites.resume = context['resume']
        favorites.employer = request.user.employer
        if not Favorites.objects.filter(resume=context['resume'], employer=request.user.employer).first():
            favorites.save()
        return self.render_to_response(context=context)


class JobseekerOfferCreateView(JobseekerViewMixin, CreateView):
    """
    Отправка отклика на вакансию.

    *Model*
    :model:`jobseekerapp.Offer`

    *Template*
    :template:`jobseekerapp/offer_create.html`
    """
    model = Offer
    template_name = 'jobseekerapp/offer_create.html'
    form_class = JobseekerOfferForm
    title = 'Отправка отклика на вакансию'

    def get_success_url(self):
        return reverse_lazy('jobseeker:cabinet', kwargs={'jobseeker_id': self.kwargs['jobseeker_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['jobseeker_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.direction = Offer.OUTGOING
        self.object.vacancy = Vacancy.objects.get(pk=self.kwargs['vacancy_id'])
        self.object.save()

        return super(JobseekerOfferCreateView, self).form_valid(form)


class JobseekerOfferListView(JobseekerViewMixin, ListView):
    """
    Просмотр отклика на вакансию.

    *Model*
    :model:`jobseekerapp.Offer`
    """
    model = Offer
    title = 'Мои отклики'

    def get_queryset(self):
        resumes = Resume.objects.filter(user=self.request.user, is_active=True)
        return super().get_queryset().filter(resume__in=resumes)

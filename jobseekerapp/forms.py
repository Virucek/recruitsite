from django import forms

from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience, Offer

DATE_INPUT_RESUME_FORMATS = [
    '%m.%Y',
    '%d.%m.%Y',
    '%Y-%m-%d',
    '%Y-%m',
]
RUB = 'RUB'
EUR = 'EUR'
USD = 'USD'
CURRENCY_CHOICES = (
    (RUB, 'RUB'),
    (EUR, 'EUR'),
    (USD, 'USD')
)


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user', 'is_active', 'failed_moderation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        status_choice = (
            (Resume.DRAFT, 'сохранить черновик'),
            (Resume.NEED_MODER, 'опубликовать на портале')
        )
        self.fields['currency'] = forms.ChoiceField(label='Валюта', choices=CURRENCY_CHOICES)
        self.fields['status'] = forms.ChoiceField(label='Выберите действие',
                                                  choices=blank_choice + status_choice)
        self.fields['key_skills'] = forms.CharField(label='Ключевые навыки', max_length=512,
                                                    widget=forms.Textarea(attrs={'rows': 4}),
                                                    )
        self.fields['about'] = forms.CharField(label='О себе', max_length=512,
                                               widget=forms.Textarea(attrs={'rows': 4}))
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_salary_max(self):
        salary_max = self.cleaned_data['salary_max']
        salary_min = self.cleaned_data['salary_min']

        if not salary_min or not salary_max:
            return salary_max
        elif salary_min > salary_max:
            raise forms.ValidationError(f'Максимальный уровень зп меньше минимального')
        else:
            return salary_max


class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        fields = ('edu_type', 'degree', 'institution_name', 'from_date', 'to_date', 'course_name',
                  'edu_description')

        class DateInput(forms.DateInput):
            input_type = 'date'

        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput()
        }

        labels = {
            'from_date': 'Дата начала',
            'to_date': 'Дата окончания'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        self.fields['edu_type'] = forms.ChoiceField(label='Тип образования',
                                                    choices=blank_choice+ResumeEducation.EDU_TYPE_CHOICES)
        self.fields['degree'] = forms.ChoiceField(label='Уровень',
                                                  choices=blank_choice+ResumeEducation.DEGREE_CHOICES)
        self.fields['edu_description'] = forms.CharField(label='Описание', max_length=512,
            widget=forms.Textarea(attrs={'rows': 4}), required=False, help_text='поле '
                                                                                'необязательное')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        from_date = self.cleaned_data['from_date']
        if to_date and from_date:
            if to_date < from_date:
                raise forms.ValidationError(f'Дата окончания раньше даты начала.')
        return to_date


class ResumeExperienceForm(forms.ModelForm):
    class Meta:
        model = ResumeExperience
        exclude = ('is_active', 'resume',)

        class DateInput(forms.DateInput):
            input_type = 'date'

        widgets = {
            'start_date': DateInput(),
            'finish_date': DateInput()
        }

        labels = {
            'start_date': 'Дата начала работы',
            'finish_date': 'Дата окончания работы'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_description'] = forms.CharField(label='Описание обязанностей',
                max_length=512, widget=forms.Textarea(attrs={'rows': 4}), help_text='Поле '
                                                                                    'необязательное', required=False)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_finish_date(self):
        finish_date = self.cleaned_data['finish_date']
        start_date = self.cleaned_data['start_date']
        if start_date and finish_date:
            if finish_date < start_date:
                raise forms.ValidationError(f'Дата окончания раньше даты начала.')
        return finish_date


class JobseekerOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('resume',
                  'cover_letter')

    def __init__(self, *args, **kwargs):
        jobseeker = kwargs.pop('jobseeker_id')
        super(JobseekerOfferForm, self).__init__(*args, **kwargs)
        self.fields['resume'].queryset = Resume.objects.filter(user=jobseeker, is_active=True)
        self.fields['resume'].empty_label = None
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

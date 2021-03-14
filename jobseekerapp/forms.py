from django import forms
from django.forms import SelectDateWidget

from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience


DATE_INPUT_RESUME_FORMATS = [
    '%m.%Y',
    '%d.%m.%Y',
    '%Y-%m-%d',
    '%Y-%m',
]
RUB = 'RUB'
EUR = 'EUR'
CURRENCY_CHOICES = (
    (RUB, 'руб.'),
    (EUR, 'EUR')
)


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user', 'is_active', 'status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'] = forms.ChoiceField(choices=CURRENCY_CHOICES)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ('salary_min', 'salary_max', 'currency'):
                field.widget.attrs['style'] = 'width: 20%; display: inline;'


class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        exclude = ('is_active', 'resume',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'] = forms.DateField(label='Дата начала', input_formats=DATE_INPUT_RESUME_FORMATS)
        self.fields['to_date'] = forms.DateField(label='Дата окончания', input_formats=DATE_INPUT_RESUME_FORMATS)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResumeExperienceForm(forms.ModelForm):
    class Meta:
        model = ResumeExperience
        exclude = ('is_active', 'resume',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'] = forms.DateField(label='Дата начала', input_formats=DATE_INPUT_RESUME_FORMATS)
        self.fields['to_date'] = forms.DateField(label='Дата окончания', input_formats=DATE_INPUT_RESUME_FORMATS)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


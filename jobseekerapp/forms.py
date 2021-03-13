from django import forms
from django.forms import SelectDateWidget

from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user_id', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        exclude = ('is_active', 'resume',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'] = forms.DateField(label='Дата начала', input_formats=['%m.%Y'])
        self.fields['to_date'] = forms.DateField(label='Дата окончания', input_formats=['%m.%Y'])
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResumeExperienceForm(forms.ModelForm):
    class Meta:
        model = ResumeExperience
        exclude = ('is_active', 'resume',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'] = forms.DateField(label='Дата начала', input_formats=['%m.%Y'])
        self.fields['to_date'] = forms.DateField(label='Дата окончания', input_formats=['%m.%Y'])
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


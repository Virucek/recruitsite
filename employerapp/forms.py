from django import forms

from authapp.models import Employer
from employerapp.models import Vacancy


class VacancyCreationForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('vacancy_name', 'vacancy_type', 'city', 'min_salary', 'max_salary', 'currency',
                  'description', 'requirements', 'conditions', 'contact_person', 'contact_email',
                  'action')

    def __init__(self, *args, **kwargs):
        super(VacancyCreationForm, self).__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        action_choice = (
            (Employer.DRAFT, 'сохранить черновик'),
            (Employer.NEED_MODER, 'опубликовать на портале')
        )
        self.fields['action'] = forms.ChoiceField(label='Выберите действие',
                                                  choices=blank_choice + action_choice)


class VacancyEditForm(forms.ModelForm):
    class Meta:
        class DateInput(forms.DateInput):
            input_type = 'date'

        model = Vacancy
        fields = ('vacancy_name', 'vacancy_type', 'city', 'min_salary', 'max_salary', 'currency',
        'description', 'requirements', 'conditions', 'contact_person', 'contact_email',
                  'hide')

    def __init__(self, *args, **kwargs):
        super(VacancyEditForm, self).__init__(*args, **kwargs)
        # blank_choice = (('', '----------'),)
        # self.fields['currency'] = forms.ChoiceField(label='Валюта', choices=blank_choice +
        # Vacancy.CURRENCY_CHOICE)
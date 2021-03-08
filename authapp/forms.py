from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from authapp.models import Jobseeker


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Имя пользователя'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Пароль'


class EmployerRegisterForm(UserCreationForm):
    INDUSTRY_TYPES = (
        ('IT', 'IT'),
        ('Banking', 'Банковские услуги'),
        ('Marketing', 'Маркетинг'),
        ('Accounting', 'Бухгалтерия'),
    )
    username = forms.CharField(label='Логин')
    company_name = forms.CharField(label='Название компании')
    email = forms.EmailField(label='Контактный e-mail')
    tax_number = forms.IntegerField(label='ИНН компании')
    phone_number = forms.IntegerField(label='Телефон компании')
    site = forms.CharField(label='Сайт компании')
    industry_type = forms.ChoiceField(label='Отрасль компании', choices=INDUSTRY_TYPES)
    short_description = forms.CharField(label='Краткое описание вашей компании', widget=forms.Textarea)
    logo = forms.ImageField(label='Ваш логотип', required=False, help_text='Необязательное поле')
    city = forms.CharField(label='Город расположения')
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Пароль')
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Подтвердите пароль')

    class Meta(UserCreationForm):
        model = User
        fields = ('username',
                  'company_name',
                  'email',
                  'tax_number',
                  'phone_number',
                  'site',
                  'industry_type',
                  'short_description',
                  'logo',
                  'city',
                  'password1',
                  'password2',
                  )

    def __init__(self, *args, **kwargs):
        super(EmployerRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            email_db = User.objects.filter(email=data)
        except User.DoesNotExist:
            email_db = None

        if email_db:
            raise forms.ValidationError(f'Пользователь с такой электронной почтой уже зарегистрирован')
        return data


class JobseekerRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя')
    middle_name = forms.CharField(label='Отчество')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Контактный e-mail')
    gender = forms.ChoiceField(label='Пол', choices=Jobseeker.GENDER_CHOICES)
    birthday = forms.DateField(label='Дата рождения', input_formats=['%d-%m-%Y', '%d.%m.%Y'])
    city = forms.CharField(label='Город', max_length=64)
    married_status = forms.ChoiceField(label='Статус в браке', choices=Jobseeker.MARRIED_STATUS_CHOICES)
    photo = forms.ImageField(label='Фото', required=False, help_text='Необязательное поле')
    phone_number = forms.CharField(label='Телефон', max_length=11)
    about = forms.CharField(label='О себе', widget=forms.Textarea, max_length=512)
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Пароль')
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Подтвердите пароль')

    class Meta(UserCreationForm):
        model = User
        fields = ('username',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'email',
                  'gender',
                  'birthday',
                  'phone_number',
                  'photo',
                  'city',
                  'married_status',
                  'about',
                  'password1',
                  'password2',
                  )

    def __init__(self, *args, **kwargs):
        super(JobseekerRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        cur_date = date.today()
        age = (cur_date - data).days // 365
        if age < 18:
            raise forms.ValidationError("Вы слишком молоды, для регистрации в качестве соискателя")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            email_db = User.objects.filter(email=data)
        except User.DoesNotExist:
            email_db = None

        if email_db:
            raise forms.ValidationError(f'Пользователь с такой электронной почтой уже зарегистрирован')
        return data

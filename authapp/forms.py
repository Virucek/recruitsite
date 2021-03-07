from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


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

    company_name = forms.CharField()
    tax_number = forms.CharField()
    phone_number = forms.CharField()
    site = forms.CharField()
    industry_type = forms.ChoiceField()
    short_description = forms.CharField()
    logo = forms.ImageField()
    city = forms.CharField()

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
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['company_name'] = forms.CharField(label='Название компании')
        self.fields['email'] = forms.EmailField(label='Контактный e-mail')
        self.fields['tax_number'] = forms.IntegerField(label='ИНН компании')
        self.fields['phone_number'] = forms.IntegerField(label='Телефон компании')
        self.fields['site'] = forms.CharField(label='Сайт компании')
        self.fields['industry_type'] = forms.ChoiceField(label='Отрасль компании',
                                                         choices=EmployerRegisterForm.INDUSTRY_TYPES)
        self.fields['short_description'] = forms.CharField(label='Краткое описание вашей компании')
        self.fields['logo'] = forms.ImageField(label='Ваш логотип', required=False,
                                               help_text='Поле необязательно')
        self.fields['city'] = forms.CharField(label='Город расположения')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

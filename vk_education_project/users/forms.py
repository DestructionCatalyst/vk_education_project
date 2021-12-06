import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import InsuranceUsers


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = InsuranceUsers
        fields = ('username', 'email', 'first_name', 'last_name', 'document_number', 'phone',
                  'birth_date', 'password', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput({'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            InsuranceUsers.objects.get(username=username)
        except InsuranceUsers.DoesNotExist:
            return username
        raise forms.ValidationError('Имя пользователя уже занято')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if re.match(r'^[A-Z][a-z]', first_name):
            return first_name
        raise ValidationError('Имя должно быть написано на латинице и начинаться с заглавной буквы')

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if re.match(r'^[A-Z][a-z]', last_name):
            return last_name
        raise ValidationError('Фамилия должна быть написано на латинице и начинаться с заглавной буквы')

    def clean_document_number(self):
        document_number = self.cleaned_data['document_number']
        if re.match(r'^[0-9]{10}$', document_number):
            return document_number
        raise ValidationError('Номер паспорта должен состоять из 10 цифр')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if re.match(r'^\+[0-9]{11}$', phone):
            return phone
        raise ValidationError('Введите кореектный номер телефона, начиная с +')

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен быть длиннее 7 символов')
        elif password.lower() == password:
            raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
        elif password.isdigit():
            raise ValidationError('Пароль не должен состоять только из чисел')
        else:
            self.cached_password = password
            return password

    def clean_password2(self):
        if self.cached_password != self.cleaned_data['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return self.cleaned_data['password2']



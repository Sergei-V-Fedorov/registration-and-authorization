from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class AuthForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Фамилия')
    birthdate = forms.DateField(help_text='Дата рождения', required=True)
    city = forms.CharField(max_length=36, required=True, help_text='Город')
    telephone = forms.CharField(max_length=10, required=False,
                                help_text='Контактный телефон')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'birthdate',
                  'city', 'telephone', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='имя')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='фамилия')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthdate',
                  'city', 'telephone']

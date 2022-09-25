from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class AuthForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField(help_text='Почта')
    login = forms.CharField(help_text='Логин(номер)')

class ActivateForm(forms.Form):
    login = forms.CharField(help_text='Логин(номер)')
    activation_code = forms.IntegerField(help_text='КОД из смс-сообщения')
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.Form):
    login = forms.CharField(help_text='Логин(номер)')
    fio = forms.CharField(max_length=50, help_text="ФИО")
    city = forms.CharField(max_length=30, help_text='город')
    job = forms.CharField(max_length=30, help_text='должность')
    foto = forms.ImageField(help_text='изображение')
    activation_code = forms.IntegerField(help_text='КОД из смс-сообщения')
    password = forms.CharField(widget=forms.PasswordInput)

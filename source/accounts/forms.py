from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    about_self = forms.CharField(required=False, max_length=2000, widget=forms.Textarea, label='О себе')
    avatar = forms.ImageField(required=False, label='avatar')
    github_profile = forms.URLField(required=False, label='Профиль на GitHub')

    class Meta:
        model = Profile
        fields = ['avatar', 'github_profile', 'about_self']


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=False, label='First name')
    last_name = forms.CharField(max_length=25, required=False, label='Last name')
    email = forms.EmailField(max_length=30, required=True, label='e-mail')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        fields_classes = {'username': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name == '' and last_name == '':
            errors.append(ValidationError('One of fields should be filled. First name or last name!'))
        if first_name == '' and last_name != '':
            return cleaned_data
        if first_name != '' and last_name == '':
            return cleaned_data
        if errors:
            raise ValidationError(errors)


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']
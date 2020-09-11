from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile


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


class ProfileForm(forms.ModelForm):
    about_self = forms.CharField(required=False, max_length=2000, widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['avatar', 'github_profile', 'about_self']

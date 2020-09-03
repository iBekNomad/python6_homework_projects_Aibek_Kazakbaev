from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        fields_classes = {'username': UsernameField}

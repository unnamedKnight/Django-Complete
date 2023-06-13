from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    fields = ['email', 'password']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})




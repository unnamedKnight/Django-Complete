from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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

    # def __init__(self, *args, **kwargs):
    #     # first call parent's constructor
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields["first_name"].required = True
    #     self.fields["last_name"].required = True


class LoginFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginFrom, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()

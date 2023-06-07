from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core import validators

User = get_user_model()


class RegistrationForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'placeholder': 'Enter Password',
    #     'class': 'form-control',
    # }), validators=[validate_password])
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'placeholder': 'Confirm Password'
    # }), validators=[validate_password])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "Password does not match!"
    #         )


class LoginFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginFrom, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core import validators

User = get_user_model()
# -------------------------------------------------------------------------------------------------------------------- #
#                                                    Important Note                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

# we can also use the UserCreationForm
# By inheriting from UserCreationForm we dont need to write any field level logic

# ------------------------------------------------------ The end ----------------------------------------------------- #


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

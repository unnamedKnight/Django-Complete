from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("user", "email_verified")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields["profile_image"].widget = forms.FileInput()

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

from django.forms import ModelForm
from .models import Profile, Skill
from django import forms


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("user", "email_verified")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # self.fields["profile_image"].widget = forms.ImageField()

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

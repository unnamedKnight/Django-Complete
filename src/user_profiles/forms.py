from django.forms import ModelForm
from .models import Profile, Skill, Message
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


class UnauthenticatedMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("name", "email", "subject", "body")

    def __init__(self, *args, **kwargs):
        super(UnauthenticatedMessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class AuthenticatedMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body")

    def __init__(self, *args, **kwargs):
        super(AuthenticatedMessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

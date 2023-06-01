from django.forms import ModelForm

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = (
            "title",
            "featured_image",
            "description",
            "demo_link",
            "tags",
            "source_code",
        )

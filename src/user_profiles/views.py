from django.shortcuts import render

from .models import Profile

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "user_profiles/profiles.html", context)


def profile_detail(request, pk):
    profile = Profile.objects.get(pk=pk)
    top_skills = Profile.objects.exclude(skill__description__iexact="")
    other_skills = Profile.objects.filter(skill__description="")
    context = {
        "profile": profile,
        top_skills: "top_skills",
        other_skills: "other_skills",
    }

    return render(request, "user_profiles/profile_detail.html", context)

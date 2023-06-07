from django.shortcuts import render

from .models import Profile

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "user_profiles/profiles.html", context)

def profile_detail(request, pk):
    profile = Profile.objects.get(pk=pk)
    context = {"profile": profile}
    return render(request, "user_profiles/profile_detail.html", context)
from django.shortcuts import render

from .models import Profile

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "user_profiles/profiles.html", context)

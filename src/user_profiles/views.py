from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "user_profiles/profiles.html", context)


def profile_detail(request, pk):
    profile = Profile.objects.get(pk=pk)
    top_skills = profile.skill_set.exclude(description__iexact="")
    other_skills = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }

    return render(request, "user_profiles/profile_detail.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, "user_profiles/account.html", context)


@login_required(login_url="login")
def edit_user_account(request):
    profile = Profile.objects.get(pk=request.user.profile.id)
    form = ProfileForm(instance=profile)

    context = {
        "form": form,
    }
    return render(request, "user_profiles/profile_form.html", context)

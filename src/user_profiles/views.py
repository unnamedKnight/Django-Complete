from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill
from .forms import ProfileForm, SkillForm
from django.contrib import messages


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
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_account")

    context = {
        "form": form,
    }
    return render(request, "user_profiles/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            messages.success(request, "Skill was added successfully.")
            return redirect("user_account")
    context = {
        "form": form,
    }
    return render(request, "user_profiles/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    skill = Skill.objects.get(pk=pk)
    if skill.owner != request.user.profile:
        return redirect("projects")
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully.")
            return redirect("user_account")
    context = {
        "form": form,
    }
    return render(request, "user_profiles/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    skill = Skill.objects.get(pk=pk)
    if skill.owner != request.user.profile:
        return redirect("user_account")
    skill.delete()
    messages.info(request, "Skill was deleted successfully.")
    return redirect("user_account")

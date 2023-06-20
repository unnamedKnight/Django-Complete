from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Profile, Skill, Message
from .forms import (
    ProfileForm,
    SkillForm,
    UnauthenticatedMessageForm,
    AuthenticatedMessageForm,
)
from django.contrib import messages


# Create your views here.


def profiles(request):
    page_num = request.GET.get("page")
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills_queryset = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(first_name__icontains=search_query)
        | Q(last_name__icontains=search_query)
        | Q(short_intro__icontains=search_query)
        # we are checking if the skills in a profile are available in
        # the skills_queryset
        | Q(skill__in=skills_queryset)
    )
    project_paginator = Paginator(profiles, 3)
    page = project_paginator.get_page(page_num)
    context = {"page": page, "search_query": search_query}
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


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messages_queryset = profile.messages.all()
    unread_messages_count = messages_queryset.filter(is_read=False).count()
    context = {
        "messages_queryset": messages_queryset,
        "unread_messages_count": unread_messages_count,
    }
    return render(request, "user_profiles/inbox.html", context)


@login_required(login_url="login")
def view_messages(request, pk):
    profile = request.user.profile
    message_obj = profile.messages.get(pk=pk)
    if message_obj.is_read is False:
        message_obj.is_read = True
        message_obj.save()
    context = {
        "message_obj": message_obj,
    }
    return render(request, "user_profiles/message.html", context)


def create_message(request, pk):
    recipient = Profile.objects.get(pk=pk)
    #- if user is logged in
    if request.user.is_authenticated:
        form = AuthenticatedMessageForm()
        if request.method == "POST":
            form = AuthenticatedMessageForm(request.POST)
            if form.is_valid():
                message_obj = form.save(commit=False)
                message_obj.sender = request.user.profile
                message_obj.recipient = recipient
                message_obj.name = request.user.profile.get_full_name()
                message_obj.email = request.user.profile.email
                message_obj.save()
                return redirect("profile_detail", pk=recipient.id)
        context = {"form": form, "recipient": recipient}
        return render(request, "user_profiles/message_form.html", context)

    form = UnauthenticatedMessageForm()
    if request.method == "POST":
        form = UnauthenticatedMessageForm(request.POST)
        if form.is_valid():
            message_obj = form.save(commit=False)
            message_obj.sender = None
            message_obj.recipient = recipient
            message_obj.save()
            return redirect("profile_detail", pk=recipient.id)
    context = {"form": form, "recipient": recipient}
    return render(request, "user_profiles/message_form.html", context)


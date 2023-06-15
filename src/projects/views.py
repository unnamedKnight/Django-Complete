from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, Tag
from .forms import ProjectForm

# Create your views here.


def projects(request):
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags_queryset = Tag.objects.filter(name=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(owner__first_name__icontains=search_query)
        | Q(owner__last_name__icontains=search_query)
        # we are checking if the tags in a project are available in
        # the tags_queryset
        | Q(tags__in=tags_queryset)
    )
    context = {"projects": projects, "search_query": search_query}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project = Project.objects.get(pk=pk)

    context = {"project": project}
    return render(request, "projects/single-project.html", context)


@login_required(login_url="login")
def create_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            messages.success(request, "Project was created successfully.")
            return redirect("project", pk=project.id)
    context = {"form": form}
    return render(request, "projects/project-form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    project = Project.objects.get(pk=pk)
    if project.owner != request.user.profile:
        return redirect("projects")
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project was updated successfully.")
            return redirect("project", pk=project.id)
    context = {"form": form}
    return render(request, "projects/project-form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if project.owner != request.user.profile:
        return redirect("projects")
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project was deleted successfully.")
        return redirect("user_account")
    context = {"project": project}
    return render(request, "projects/delete-project.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

# Create your views here.


def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
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
            form.save(owner=request.user.profile)
            # project = form.save(commit=False)
            # project(owner=request.user.profile)
            # project.save()
            return redirect("projects")
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
            return redirect("projects")
    context = {"form": form}
    return render(request, "projects/project-form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if project.owner != request.user.profile:
        return redirect("projects")
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {"project": project}
    return render(request, "projects/delete-project.html", context)

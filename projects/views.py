from django.shortcuts import render, redirect
from .models import Project, Tag
from users.models import Profile
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects, projectPagination


# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    paginator, projects, custom_range = projectPagination(request, projects)

    context = {'projects': projects, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    # get the specific item from Project with an ID that matches the Primary key
    projectObj = Project.objects.get(id=pk)
    # get the manytomany items linked to the project object
    # tags = projectObj.tags.all()
    context = {'projectObj': projectObj}
    return render(request, 'projects/project.html', context)


# decorator that requires a user to be logged in to access
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    # IMPORTANT: ensures that only the logged in user can access/edit their projects
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
# delete an existing project
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_obj.html', context)



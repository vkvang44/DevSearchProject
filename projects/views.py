from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm


# Create your views here.
def projects(request):
    # query the items from Project into the variable proj
    projectsObj = Project.objects.all()
    context = {'projects': projectsObj}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    # get the specific item from Project with an ID that matches the Primary key
    projectObj = Project.objects.get(id=pk)
    # get the manytomany items linked to the project object
    # tags = projectObj.tags.all()
    context = {'projectObj': projectObj}
    return render(request, 'projects/project.html', context)


# create a new project
def createProject(request):
    # create an instance of this class
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


# updated an existing project
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    # create an instance of this class
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)
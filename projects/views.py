from django.shortcuts import render
from .models import Project


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
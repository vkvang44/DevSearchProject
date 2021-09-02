from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


# Create your views here.
def projects(request):
    # query the items from Project into the variable proj
    projectsObj = Project.objects.all()
    context = {'projects': projectsObj}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {'projectObj': projectObj}
    return render(request, 'projects/project.html', context)
from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, projectPagination
from django.contrib import messages


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

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        # update total vote count
        projectObj.getVoteCount
        messages.success(request, 'Your review has been posted!')
        return redirect('project', pk=projectObj.id)
    context = {'projectObj': projectObj, 'form':form}
    return render(request, 'projects/project.html', context)


# decorator that requires a user to be logged in to access
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newTags = request.POST.get('newTags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
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
        newTags = request.POST.get('newTags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form, 'project':project}
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



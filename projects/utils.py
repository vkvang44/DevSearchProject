from .models import Project, Tag
from django.db.models import Q

def searchProjects(request):
    # query the items from Project into the variable proj
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # IMPORTANT: I can reference the parent obj of a child instead of having to create its own query set
    # variable like tag or skill (ie. owner__name__icontains)
    tag = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                 Q(tags__in=tag) |
                                                 Q(owner__name__icontains=search_query)
                                                 )

    return projects, search_query
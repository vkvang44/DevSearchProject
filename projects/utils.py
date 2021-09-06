from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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


def projectPagination(request, projects):
    """
    page represents the current page user is on, result equals how many items displayed per page, paginator creates
    an instance of the method Paginator that allows the projects to be displayed

    try: displays the projects associated with the page number passed in
    Except PageNotAnInteger: displays the first page when users click on projects tab
    Except EmptyPage: takes user to the last page if they input a page number gt set amount of pages

    leftIndex/rightIndex limits the range of page buttons displayed on website. If total pages = 1000 and leftIndex = 1,
    rightIndex = 10 then only 10 buttons display
    """
    page = request.GET.get('page')
    result = 6
    paginator = Paginator(projects, result)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)
    rightIndex = (int(page) + 5)
    if leftIndex < 1:
        leftIndex = 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return paginator, projects, custom_range
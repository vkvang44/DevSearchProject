"""
utils.py is a great  file for helper functions that i can call in my views. The purpose of this file is to
create cleaner code and separate functions. Just import the file in my views when I need a helper function
"""
from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfiles(request):
    # based on method="GET" inside a form tag. If it is triggered then a search_query will be populated with user
    # inputted string
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # will filter the profiles depending on search_query string
    # Queue search with Q() | Q() will look for one or the other with "| = or"
    # Q(skill__in=skill) -> we want to know if the profile object contains a skill object within the skill query set
    # variable
    skill = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                      Q(short_intro__icontains=search_query) |
                                      Q(skill__in=skill)
                                      )
    return profiles, search_query

def profilePagination(request, profiles):
    """
    page represents the current page user is on, result equals how many items displayed per page, paginator creates
    an instance of the method Paginator that allows the profiles to be displayed

    try: displays the projects associated with the page number passed in
    Except PageNotAnInteger: displays the first page when users click on projects tab
    Except EmptyPage: takes user to the last page if they input a page number gt set amount of pages

    leftIndex/rightIndex limits the range of page buttons displayed on website. If total pages = 1000 and leftIndex = 1,
    rightIndex = 10 then only 10 buttons display
    """
    page = request.GET.get('page')
    result = 9
    paginator = Paginator(profiles, result)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    rightIndex = (int(page) + 5)
    if leftIndex < 1:
        leftIndex = 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return paginator, profiles, custom_range
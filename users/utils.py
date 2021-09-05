"""
utils.py is a great  file for helper functions that i can call in my views. The purpose of this file is to
create cleaner code and separate functions. Just import the file in my views when I need a helper function
"""
from .models import Profile, Skill
from django.db.models import Q


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
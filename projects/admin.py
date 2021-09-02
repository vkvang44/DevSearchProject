from django.contrib import admin
from.models import Project


# Register your models here after you have created the tables in your models.py to see them in /admin
from.models import Project

admin.site.register(Project)

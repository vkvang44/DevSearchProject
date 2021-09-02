from django.contrib import admin

# Register your models here after you have created the tables in your models.py to see them in /admin
from.models import Project, Review, Tag

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    # the model we are creating the form for
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags', 'featured_image']
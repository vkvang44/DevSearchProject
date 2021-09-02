from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    # the model we are creating the form for
    class Meta:
        model = Project
        fields = '__all__'
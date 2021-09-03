from django.forms import ModelForm
from .models import Project
from django import forms


class ProjectForm(ModelForm):
    # the model we are creating the form for
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        #self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Project Name',})
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

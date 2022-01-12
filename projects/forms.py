from django.forms import ModelForm
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    # the model we are creating the form for
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        #self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Project Name',})
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Project Name',})
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            if field_name == 'body':
                self.fields['body'].widget.attrs.update({'placeholder': 'Add a comment with your vote...'})
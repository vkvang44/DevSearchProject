from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message #Experience
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input', })


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email', 'username', 'profile_image', 'short_intro', 'bio', 'location',
                  'social_github', 'social_twitter', 'social_linkedin', 'social_stackoverflow',
                  'social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input', })

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input', })


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input', })

#
# class ExperienceForm(ModelForm):
#     class Meta:
#         model = Experience
#         fields = ['title', 'company', 'description']
#
#     def __init__(self, *args, **kwargs):
#         super(ExperienceForm, self).__init__(*args, **kwargs)
#
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input', })
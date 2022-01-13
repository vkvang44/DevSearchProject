from django.db import models
import uuid
from users.models import Profile


# Create your models here.
class Project(models.Model):
    # user models.foreignKey to create a many-to-one relationship ( project(many) - profiles(one) )
    owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)

    # table models that appear in admin database
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    '''
    IMPORTANT!!!
    When I create an imagefield model, I need to make some configurations to MEDIA_ROOT in the settings.py 
    to make sure that user uploaded images go into the static/images folders so it does not pollute my
    files
    
    created an image field model that allows users to upload images
    '''
    featured_image = models.ImageField(null=True, blank=True, default='projects/default.jpg', upload_to="projects/")

    # create a connection from project to tags, project to Review
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    # add in str method to get the title name to render in admin
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = 'http://127.0.0.1:8000/images/profiles/user-default.png'
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


# created a one to many relationship table ( project -> review )
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        # makes sure each profile only has 1 review per project
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


# created a many to many relationship table (project -> Tag)
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
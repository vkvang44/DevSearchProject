from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project
from users.models import Profile


# Create your tests here.
class ProjectModelTest(TestCase):
    @classmethod
    def setUp(cls):
        User.objects.create_superuser(username='user1', password='testpassword', email='user1@email.com')
        cls.profile = Profile.objects.get(username="user1")
        cls.project = Project.objects.create(owner=cls.profile, title="Test Project", description="Test Desc")

    def testProjectCreation(self):
        self.assertEqual(self.project.owner, self.profile)
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.description, "Test Desc")


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Skill, Message, Experience


class ProfileModelTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='user1', password='testpassword', email='user1@email.com')

    def testProfileCreation(self):
        profile = Profile.objects.get(username="user1")
        user = profile.user
        username = profile.username
        email = profile.email
        self.assertEqual(user, User.objects.get(username="user1"))
        self.assertEqual(username, "user1")
        self.assertEqual(email, "user1@email.com")


class SkillModelTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='user1', password='testpassword', email='user1@email.com')
        profile = Profile.objects.get(username="user1")
        Skill.objects.create( owner=profile, name="HTML", description="HELLO")

    def testSkillCreation(self):
        skill = Skill.objects.get(name="HTML")
        self.assertEqual(skill.owner, Profile.objects.get(username="user1"))
        self.assertEqual(skill.name, "HTML")
        self.assertEqual(skill.description, "HELLO")


class MessageModelTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='user1', password='testpassword', email='user1@email.com')
        User.objects.create_superuser(username='user2', password='testpassword', email='user2@email.com')
        sender = Profile.objects.get(username="user1")
        recipient = Profile.objects.get(username="user2")
        Message.objects.create(sender=sender, recipient=recipient, name='user1', email='user1@email.com', subject='test', body="Hello!")

    def testMessageCreation(self):
        message = Message.objects.get(subject='test')
        sender = Profile.objects.get(username="user1")
        recipient = Profile.objects.get(username="user2")
        self.assertEqual(message.sender, sender)
        self.assertEqual(message.recipient, recipient)
        self.assertEqual(message.name, "user1")
        self.assertEqual(message.email, "user1@email.com")
        self.assertEqual(message.subject, "test")


# class based testing allows for quicker testing by referencing class
class ExperienceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='user1', password='testpassword', email='user1@email.com')
        cls.profile = Profile.objects.get(username="user1")
        cls.exp = Experience.objects.create(owner=cls.profile, title='title', company='company', description='desc')

    def testExperienceCreation(self):
        self.assertEqual(self.exp.owner, self.profile)
        self.assertEqual(self.exp.title, 'title')
        self.assertEqual(self.exp.company, 'company')
        self.assertEqual(self.exp.description, 'desc')

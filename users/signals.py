"""
Signals are a great way to activate specific actions by "listening" to what actions are performed by the user on the
website. In this instance, I am creating two methods: First, is the createProfile method that automatically
creates a profile associated with the user when a new user is created. Second, is the deleteUser method that
will delete the user if the profile associated with that user is deleted.

Gotta make sure to setup the connection in the apps.py to make sure django can communicate with signals.py file
"""

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

# this methods checks if user if being created for the first time after a save(). if true, then it creates a profile
# for the new user
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )



def updateProfile(sender, instance, created, **kwargs):
    # have to set it up like this to access the 1-to-1 relationship of profile and user
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


# IMPORTANT: the .connect sets up the connections between the method and an instance of the object that will passed
# to the method
post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
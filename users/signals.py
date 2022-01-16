from pickle import FALSE
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# @receiver(post_save, sender=Profile)
def createProfile(sender,instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            users = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )
def updateUser(sender,instance,created, **kwargs):
    profile=instance
    user=profile.users
    if created== FALSE :
        user.first_name= profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()


def profileDeleted(sender,instance, **kwargs):
    print("Profile Deleted!")

post_save.connect(createProfile, sender = User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(profileDeleted, sender = Profile)
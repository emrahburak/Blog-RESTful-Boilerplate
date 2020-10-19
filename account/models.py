from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=120)
    twitter = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profie(sender, instance, created, **kwargs):
    user = instance
    
    if created:
        profile = Profile(user=user)
        profile.save()

        #Profile.objects.create(user=instance)


        #instance.profile.save()

    

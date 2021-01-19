from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    signup_confirmation = models.BooleanField(default=False)
    firstName = models.CharField(max_length=40, blank = True)
    lastName = models.CharField(max_length=40, blank= True)
    email = models.EmailField(max_length=250, blank = True)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    instance.profile.save()
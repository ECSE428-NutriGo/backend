from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    protein_target = models.IntegerField(default=0)
    carb_target = models.IntegerField(default=0)
    fat_target = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Create a matching profile whenever a user object is created.
    if created: 
        profile, new = Profile.objects.get_or_create(user=instance)
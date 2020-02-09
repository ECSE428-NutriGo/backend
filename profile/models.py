from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    protein_target = models.IntegerField(default=0)
    carb_target = models.IntegerField(default=0)
    fat_target = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
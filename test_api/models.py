from django.db import models
from django.db.models.base import Model


# Create your models here.

class PersonalProfile(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=10)
    birthday = models.DateTimeField()
    job = models.CharField(max_length=32)
    interest = models.TextField(null=True)
    skill = models.TextField(null=True)
    wantingToLearn = models.TextField(null=True)
    
    
    def __str__(self):
        return "{}: {}".format(self.pk, self.username)
    
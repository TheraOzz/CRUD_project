from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Trainer(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)
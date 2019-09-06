from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class SlackUser(AbstractUser):
    slack_id = models.CharField(max_length=9, primary_key=True)
    avatar = models.URLField()
    access_token = models.CharField(max_length=128)

    def __str__(self):
        return self.username

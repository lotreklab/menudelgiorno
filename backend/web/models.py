from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from app.models import Course


class SlackUser(AbstractUser):
    slack_id = models.CharField(max_length=9, primary_key=True)
    avatar = models.URLField()
    access_token = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Review(models.Model):
    class Meta:
        unique_together = (('course', 'user'),)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    text = models.TextField(max_length=2048, null=True)

    def get_score_list(self):
        return [True for i in range(self.score)] + [False for i in range(5 - self.score)]

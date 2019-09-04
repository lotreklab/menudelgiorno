from django.db import models
from polymorphic.models import PolymorphicModel

FIRST_CONTENT_TYPES = [('0', 'Terra'), ('1', 'Mare')]
SECOND_CONTENT_TYPES = [('0', 'Terra'), ('1', 'Insalatona')]
SIDE_COOKING_TYPES = [('0', 'Vapore'), ('1', 'Forno'), ('2', 'Non definito')]

class Course(PolymorphicModel):
    name = models.CharField(max_length=30)

class FirstCourse(Course):
    contentType = models.CharField(max_length=1, choices=FIRST_CONTENT_TYPES)

class SecondCourse(Course):
    contentType = models.CharField(max_length=1, choices=SECOND_CONTENT_TYPES)
    
class SideCourse(Course):
    cookingType = models.CharField(max_length=1, choices=SIDE_COOKING_TYPES)

class Menu(models.Model):
    consumeDate = models.DateField(auto_now_add=True)
    sendDate = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField(Course, through='ContentMenu')

class ContentMenu(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    price = models.FloatField()

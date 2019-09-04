from django.db import models
from polymorphic.models import PolymorphicModel

FIRST_CONTENT_TYPES = [('T', 'Terra'), ('M', 'Mare')]
FIRST_COOKING_TYPES = [('C', 'Caldo'), ('F', 'Freddo')]
SECOND_CONTENT_TYPES = [('T', 'Terra'), ('I', 'Insalatona')]
SIDE_COOKING_TYPES = [('V', 'Vapore'), ('F', 'Forno'), ('N', 'Non definito')]


class Course(PolymorphicModel):
    name = models.CharField(max_length=30, unique=True)
    notes = models.TextField(max_length=2048, null=True)


class FirstCourse(Course):
    contentType = models.CharField(max_length=1, choices=FIRST_CONTENT_TYPES)
    cookingType = models.CharField(max_length=1, choices=FIRST_COOKING_TYPES)


class SecondCourse(Course):
    contentType = models.CharField(max_length=1, choices=SECOND_CONTENT_TYPES)


class SideCourse(Course):
    cookingType = models.CharField(max_length=1, choices=SIDE_COOKING_TYPES)


class Menu(models.Model):
    consumeDate = models.DateField()
    sendDate = models.DateTimeField()
    courses = models.ManyToManyField(Course, through='ContentMenu')


class ContentMenu(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    price = models.FloatField()

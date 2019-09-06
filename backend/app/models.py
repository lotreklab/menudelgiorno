from django.db import models
from polymorphic.models import PolymorphicModel

FIRST_CONTENT_TYPES = [('T', 'Terra'), ('M', 'Mare')]
FIRST_COOKING_TYPES = [('C', 'Caldo'), ('F', 'Freddo')]
SECOND_CONTENT_TYPES = [('T', 'Terra'), ('I', 'Insalatona')]
SIDE_COOKING_TYPES = [('V', 'Vapore'), ('F', 'Forno'), ('N', 'Non definito')]


class Course(PolymorphicModel):
    name = models.CharField(max_length=30, unique=True)
    notes = models.TextField(max_length=2048, null=True)

    def __str__(self):
        return self.name.capitalize()


class FirstCourse(Course):
    contentType = models.CharField(max_length=1, choices=FIRST_CONTENT_TYPES)
    cookingType = models.CharField(max_length=1, choices=FIRST_COOKING_TYPES)

    def description(self):
        dish_notes = "Primo %s di %s\n" % (self.get_cookingType_display().lower(),
                                           self.get_contentType_display().lower())
        return dish_notes


class SecondCourse(Course):
    contentType = models.CharField(max_length=1, choices=SECOND_CONTENT_TYPES)

    def __str__(self):
        return ("Insalatona %s" if self.contentType == 'I' else "%s") % super().__str__()

    def description(self):
        dish_notes = ("Secondo di %s" if self.contentType == 'T' else "%s") % self.get_contentType_display()
        return dish_notes


class SideCourse(Course):
    cookingType = models.CharField(max_length=1, choices=SIDE_COOKING_TYPES)

    def __str__(self):
        if self.cookingType != 'N':
            return "%s al %s" % (super().__str__(), self.get_cookingType_display().lower())
        else:
            return super().__str__()

    def description(self):
        dish_notes = "Contorno con cottura al %s" % self.get_cookingType_display().lower() if self.cookingType != 'N' else "Contorno semplice"
        return dish_notes


class Menu(models.Model):
    consumeDate = models.DateField()
    sendDate = models.DateTimeField()
    courses = models.ManyToManyField(Course, through='ContentMenu')


class ContentMenu(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    price = models.FloatField()

from django.contrib import admin

# Register your models here.
from app.models import Menu
from app.models import Course

admin.site.register(Menu)
admin.site.register(Course)
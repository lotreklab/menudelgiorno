from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from app import models
from app import serializers
from app.models import Menu, ContentMenu, Course

class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CoursePolymorphicSerializer
    
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

class ContentMenuViewSet(viewsets.ModelViewSet):
    queryset = ContentMenu.objects.all()
    serializer_class = serializers.ContentMenuSerializer
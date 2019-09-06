from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from app import models
from app import serializers
from app.models import Menu, ContentMenu, Course

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @action(detail=False, methods=['get'])
    def get_from_nome(self, request):
        courses = Course.objects.filter(name=self.request.query_params.get('name'))
        serializer = serializers.CourseSerializer(courses, many=True)
        return Response(serializer.data)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

class ContentMenuViewSet(viewsets.ModelViewSet):
    queryset = ContentMenu.objects.all()
    serializer_class = serializers.ContentMenuSerializer
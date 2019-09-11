from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from app import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'name']


class FirstCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FirstCourse
        fields = ['id', 'name', 'content_type']


class SecondCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecondCourse
        fields = ['id', 'name', 'content_type']


class SideCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SideCourse
        fields = ['id', 'name', 'cooking_type']


class CoursePolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'category'
    model_serializer_mapping = {
        models.Course: CourseSerializer,
        models.FirstCourse: FirstCourseSerializer,
        models.SecondCourse: SecondCourseSerializer,
        models.SideCourse: SideCourseSerializer
    }


class ContentMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentMenu
        fields = ['course', 'menu', 'price']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = ['id', 'consume_date', 'send_date', 'courses']

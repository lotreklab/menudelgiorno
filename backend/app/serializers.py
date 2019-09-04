from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from app import models

class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Menu
        fields = ['id', 'consumeDate', 'sendDate']

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'name']

class FirstCourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FirstCourse
        fields = ['id', 'contentType']

class SecondCourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SecondCourse
        fields = ['id', 'contentType']

class SideCourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SideCourse
        fields = ['id', 'cookingType']
        
class CoursePolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'category'
    model_serializer_mapping = {
        models.Course: CourseSerializer,
        models.FirstCourse: FirstCourseSerializer,
        models.SecondCourse: SecondCourseSerializer,
        models.SideCourse: SideCourseSerializer
    }

class ContentMenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ContentMenu
        fields = ['course', 'menu', 'price']

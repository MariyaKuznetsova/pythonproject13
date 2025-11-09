from rest_framework import serializers

from study.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор по курсам"""
    class Meta:
        model = Course
        fields = ["name", "description"]


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор по урокам"""
    class Meta:
        model = Lesson
        fields = ["name", "description", "courses"]
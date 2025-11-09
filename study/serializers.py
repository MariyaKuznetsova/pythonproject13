from rest_framework import serializers

from study.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор по урокам"""
    class Meta:
        model = Lesson
        fields = ["name", "description", "courses"]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор по курсам"""
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["name", "description", "lessons"]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор по курсам с добавлением поля с количеством уроков"""
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ["name", "description", "lessons", "lesson_count"]






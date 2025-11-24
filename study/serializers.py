from rest_framework import serializers

from study.models import Course, Lesson, Subscription
from study.validators import validate_forbidden_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор по урокам"""

    video = serializers.URLField(validators=[validate_forbidden_url])

    class Meta:
        model = Lesson
        fields = ["name", "description", "courses", "video"]


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


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор по подпискам"""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        course = obj.course_subscription
        return Subscription.objects.filter(
            user_subscription=user, course_subscription=course
        )

    class Meta:
        model = Subscription
        fields = ["user_subscription", "course_subscription", "is_subscribed"]

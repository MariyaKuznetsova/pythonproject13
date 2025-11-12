from rest_framework import generics, viewsets

from study.models import Course, Lesson
from study.serializers import (CourseDetailSerializer, CourseSerializer,
                               LessonSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер по курсу"""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер по созданию урока"""

    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Контроллер по выводу списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер по выводу урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер по редактированию урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер по удаления урока"""

    serializer_class = LessonSerializer

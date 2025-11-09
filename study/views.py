from rest_framework import viewsets, generics

from study.models import Course, Lesson
from study.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер по курсу"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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
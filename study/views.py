from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from study.models import Course, Lesson
from study.serializers import (CourseDetailSerializer, CourseSerializer,
                               LessonSerializer)
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер по курсу"""

    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner)
        if self.action == "destroy":
            self.permission_classes = (~IsModer, IsOwner)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер по созданию урока"""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    """Контроллер по выводу списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer, IsOwner)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер по выводу урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer, IsOwner)

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер по редактированию урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer, IsOwner)

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер по удаления урока"""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer, IsOwner)
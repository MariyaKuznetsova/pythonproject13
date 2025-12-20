from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from study.models import Course, Lesson, Subscription
from study.paginators import MyPagination
from study.serializers import (CourseDetailSerializer, CourseSerializer,
                               LessonSerializer, SubscriptionSerializer)
from study.tasks import send_information_about_subscription
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер по курсу"""

    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPagination

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
            self.permission_classes = IsModer | IsOwner
        if self.action == "destroy":
            self.permission_classes = (~IsModer, IsOwner)
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        subscriptions = Subscription.objects.filter(course=course)
        for subscription in subscriptions:
            send_information_about_subscription.delay(
                subscription.user_subscription.email
            )


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер по созданию урока"""

    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Контроллер по выводу списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
    pagination_class = MyPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер по выводу урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер по редактированию урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер по удаления урока"""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
    queryset = Lesson.objects.all()


class SubscriptionAPIView(APIView):
    """Контроллер по установки подписки пользователя и на удаление подписки у пользователя."""

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_subscription")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(
            user_subscription=user, course_subscription=course_item
        )

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(
                user_subscription=user, course_subscription=course_item
            )
            message = "подписка добавлена"
            return Response({"message": message}, status=status.HTTP_201_CREATED)

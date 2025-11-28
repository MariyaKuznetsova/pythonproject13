from django.urls import path
from rest_framework.routers import SimpleRouter

from study.apps import StudyConfig
from study.views import (CourseViewSet, LessonCreateAPIView,
                         LessonDestroyAPIView, LessonListAPIView,
                         LessonRetrieveAPIView, LessonUpdateAPIView,
                         SubscriptionAPIView)

app_name = StudyConfig.name

router = SimpleRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
] + router.urls
